import json
from datetime import date
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def fetch_as_dict(cursor): #-> Essa função é um helper para transformar os resultados do cursor do banco em uma lista de dicionários, onde cada dicionário representa uma linha da tabela, com as chaves sendo os nomes das colunas
    colunas = [col[0] for col in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]


# ------------------------- LOGIN -------------------------
@csrf_exempt 
#O método realizar_login é responsável por autenticar os usuários (donos) que tentam acessar o sistema. Ele recebe uma requisição POST com o usuario e senha, verifica essas credenciais no banco de dados, e retorna uma resposta JSON indicando se o login foi bem-sucedido ou não, junto com os dados do usuário logado em caso de sucesso. Ele também lida com erros e casos de usuário não encontrado ou senha incorreta, retornando mensagens apropriadas para o frontend.
def realizar_login(request): 
    if request.method == 'POST': 
        try:
            dados = json.loads(request.body) 
            usuario_input = dados.get('email')
            senha_input = dados.get('senha')

            with connection.cursor() as cursor:
                # Buscando o usuário específico no banco
                cursor.execute(""" 
                    SELECT nome, senha, perfil 
                    FROM dono 
                    WHERE usuario = %s
                """, [usuario_input])
                
                row = cursor.fetchone() 

            if not row: # Se a query não retornar nada, significa que o usuário não existe
                return JsonResponse({'sucesso': False, 'mensagem': 'Usuário não encontrado.'}, status=401)
            
            
            if row[1] != senha_input: # row[1] é a senha do banco, e senha_input é a senha que o usuário digitou. Se forem diferentes, a senha está incorreta.
                return JsonResponse({'sucesso': False, 'mensagem': 'Senha incorreta.'}, status=401)
            
            return JsonResponse({ # Retorna os dados do usuário logado
                'sucesso': True, 
                'nome_usuario': row[0],
                'perfil': row[2] or 'Dono' 
            })

        except Exception as e: # Se der qualquer erro durante o processo de login, retornamos uma mensagem de erro genérica para o frontend, e logamos o erro real no console para ajudar no debug.
            return JsonResponse({'sucesso': False, 'mensagem': f'Erro: {str(e)}'}, status=500)
    return JsonResponse({'sucesso': False, 'mensagem': 'Método inválido.'}, status=405)


# ------------------------- PROPRIETÁRIOS (Dono) -------------------------
@csrf_exempt
#O método gerenciar_proprietarios é responsável por lidar com as requisições relacionadas aos donos (proprietários) dos animais. Ele suporta os métodos GET para listar os donos e POST para criar um novo dono. No GET, ele busca os donos no banco, conta quantos animais cada dono possui, e formata os dados para o frontend. No POST, ele insere um novo dono no banco e retorna o ID do dono criado.
def gerenciar_proprietarios(request):
    # O método retorna a lista de donos, e o POST cria um novo dono.
    if request.method == 'GET': 
        with connection.cursor() as cursor:
            # Contar os animais direto na busca do dono
            cursor.execute("""
                SELECT d.id_dono, d.nome, d.usuario, d.telefone, d.status_dono,
                       d.cor_brinco, d.descricao_marca, d.perfil,
                       (SELECT COUNT(*) FROM animal a WHERE a.id_dono = d.id_dono) as total_animais
                FROM dono d
                ORDER BY d.nome
            """)
            donos = fetch_as_dict(cursor)
            
            # Tratamento de nulos para o frontend não quebrar
            for d in donos:
                d['telefone'] = d['telefone'] or 'Não informado'
                d['descricao_marca'] = d['descricao_marca'] or 'Sem marca'
                d['perfil'] = d['perfil'] or 'Dono'
                
        return JsonResponse(donos, safe=False)
    
#Método POST para criar um novo dono, recebendo os dados do frontend, inserindo no banco, e retornando o ID do dono criado 
    elif request.method == 'POST': 
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                # Devolve o ID gerado pelo banco serial imediatamente
                cursor.execute("""
                    INSERT INTO dono (nome, usuario, senha, status_dono, telefone, cor_brinco, descricao_marca, perfil)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id_dono
                """, [
                    dados.get('nome'), dados.get('usuario'), dados.get('senha', '123456'), 
                    dados.get('status_dono', 'A'), dados.get('telefone', ''), dados.get('cor_brinco', ''), 
                    dados.get('descricao_marca', ''), dados.get('perfil', 'Dono')
                ])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'sucesso': True, 'id_dono': novo_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
#O método atualiza os dados do dono
def detalhe_proprietario(request, id_dono):
    if request.method == 'PUT': 
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                # COALESCE usa o dado novo, mas se vier vazio (NULL), mantém o dado antigo do banco
                cursor.execute("""
                    UPDATE dono 
                    SET nome = COALESCE(%s, nome),
                        usuario = COALESCE(%s, usuario),
                        telefone = COALESCE(%s, telefone),
                        status_dono = COALESCE(%s, status_dono),
                        descricao_marca = COALESCE(%s, descricao_marca),
                        perfil = COALESCE(%s, perfil)
                    WHERE id_dono = %s
                """, [
                    dados.get('nome'), dados.get('usuario'), dados.get('telefone'),
                    dados.get('status_dono'), dados.get('descricao_marca'), dados.get('perfil'), id_dono
                ])
                
                # Se a pessoa mandou senha nova, fazemos um UPDATE separado para a senha
                if 'senha' in dados and dados['senha'].strip() != '':
                    cursor.execute("UPDATE dono SET senha = %s WHERE id_dono = %s", [dados['senha'], id_dono])

            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            # O Cascade no banco resolve os animais, mas deletamos o dono aqui
            cursor.execute("DELETE FROM dono WHERE id_dono = %s", [id_dono])
        return JsonResponse({'sucesso': True})


# ------------------------- ANIMAIS -------------------------
@csrf_exempt
#O método gerenciar_animais é responsável por lidar com as requisições relacionadas aos animais. Ele suporta os métodos GET para listar os animais e POST para criar um novo animal. No GET, ele busca os animais no banco, junta as informações do dono, categoria e leilão usando LEFT JOINs, e formata os dados para o frontend. No POST, ele insere um novo animal no banco e retorna o ID do animal criado.
def gerenciar_animais(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id_animal as id, a.numero_brinco as nome, a.raca, a.status, a.sexo, 
                       a.peso, a.dt_nasc, d.nome as dono_nome, c.descricao as categoria_desc,
                       COALESCE(l.nome_evento, 'Não vinculado') as leilao_nome,
                       a.id_dono, a.id_categoria, a.id_leilao
                FROM animal a
                LEFT JOIN dono d ON a.id_dono = d.id_dono
                LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
                LEFT JOIN leilao l ON a.id_leilao = l.id_leilao
                ORDER BY d.nome ASC
            """)
            
           # Transformar o resultado em lista de dicionários
            colunas = [col[0] for col in cursor.description]
            animais = [dict(zip(colunas, row)) for row in cursor.fetchall()]
            
            # Tratamento de nulos e formatação para o frontend
            for a in animais:
                a['peso'] = float(a['peso']) if a['peso'] else 0.0
                a['dt_nasc'] = a['dt_nasc'].strftime('%Y-%m-%d') if a['dt_nasc'] else ''
                
        return JsonResponse(animais, safe=False)
        
    #O método POST para criar um novo animal, recebendo os dados do frontend, inserindo no banco, e retornando o ID do animal criado    
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO animal (numero_brinco, raca, status, sexo, peso, dt_nasc, id_dono, id_categoria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_animal
                """, [
                    dados.get('nome', ''), dados.get('raca', ''), dados['status'], dados['sexo'],
                    dados['peso'], dados.get('dt_nasc', '2024-01-01'), dados['id_dono'], dados['id_categoria']
                ])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'id': novo_id, 'sucesso': True}, status=201)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

@csrf_exempt
#O método detalhe_animal é responsável por lidar com as requisições relacionadas a um animal específico, identificado pelo id_animal. Ele suporta os métodos GET para obter os detalhes do animal, PUT para atualizar os dados do animal, e DELETE para remover o animal do banco. No PUT, ele usa a função COALESCE para atualizar apenas os campos que foram enviados no corpo da requisição, mantendo os valores antigos para os campos que não foram enviados.
def detalhe_animal(request, id_animal):
    if request.method == 'PUT':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE animal 
                    SET numero_brinco = COALESCE(%s, numero_brinco),
                        raca = COALESCE(%s, raca),
                        status = COALESCE(%s, status),
                        sexo = COALESCE(%s, sexo),
                        peso = COALESCE(%s, peso),
                        id_dono = COALESCE(%s, id_dono),
                        id_categoria = COALESCE(%s, id_categoria)
                    WHERE id_animal = %s
                """, [
                    dados.get('nome'), dados.get('raca'), dados.get('status'), dados.get('sexo'),
                    dados.get('peso'), dados.get('id_dono'), dados.get('id_categoria'), id_animal
                ])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM animal WHERE id_animal = %s", [id_animal])
        return JsonResponse({'sucesso': True})


# ------------------------- CATEGORIAS -------------------------
@csrf_exempt
def gerenciar_categorias(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_categoria, descricao, nome_categoria FROM categoria ORDER BY id_categoria")
            categorias = fetch_as_dict(cursor)
        return JsonResponse(categorias, safe=False)
        
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categoria (descricao, nome_categoria) 
                    VALUES (%s, %s) RETURNING id_categoria
                """, [dados['descricao'], dados['nome_categoria']])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'id': novo_id, 'sucesso': True}, status=201)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
        
@csrf_exempt
def detalhe_categoria(request, id_categoria): #O id_categoria vem da URL, e é usado para identificar qual categoria estamos buscando, editando ou deletando. Ele é passado como argumento para a função detalhe_categoria, e depois usado nas queries SQL para filtrar pela categoria correta.
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_categoria, descricao, nome_categoria FROM categoria WHERE id_categoria = %s", [id_categoria])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({'erro': 'Categoria não encontrada'}, status=404)
            
            return JsonResponse({
                'id': row[0],
                'descricao': row[1],
                'nome_categoria': row[2]
            })

    elif request.method == 'PUT':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE categoria 
                    SET descricao = COALESCE(%s, descricao),
                        nome_categoria = COALESCE(%s, nome_categoria)
                    WHERE id_categoria = %s
                """, [dados.get('descricao'), dados.get('nome_categoria'), id_categoria])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", [id_categoria])
        return JsonResponse({'sucesso': True})


# ------------------------- LEILÕES -------------------------
import datetime # Necessário para converter strings em datas de forma segura
from datetime import date

@csrf_exempt
#O método gerenciar_leiloes é responsável por lidar com as requisições relacionadas aos leilões. Ele suporta os métodos GET para listar os leilões e POST para criar um novo leilão. No GET, ele busca os leilões no banco, formata as datas e associa os animais vinculados a cada leilão. No POST, ele insere um novo leilão no banco e vincula os animais selecionados a esse leilão usando o operador ANY do PostgreSQL para atualizar múltiplos registros de uma vez.
def gerenciar_leiloes(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_leilao, nome_evento, dt_leilao, custo_fixo, local FROM leilao ORDER BY dt_leilao")
            leiloes = fetch_as_dict(cursor)
            
            # Busca todos os animais que têm um leilão vinculado
            cursor.execute("SELECT id_animal as id, numero_brinco as nome, raca, id_leilao FROM animal WHERE id_leilao IS NOT NULL")
            animais_vinculados = fetch_as_dict(cursor)
            
            hoje = date.today()
            
            for l in leiloes:
                # PROTEÇÃO 1: Evita erro se o custo fixo for NULL no banco
                l['custo_fixo'] = float(l['custo_fixo']) if l['custo_fixo'] is not None else 0.0
                
                # PROTEÇÃO 2: Garante que a data seja um objeto "date" e não uma "string"
                dt_leilao_obj = l['dt_leilao']
                if isinstance(dt_leilao_obj, str):
                    try:
                        dt_leilao_obj = datetime.datetime.strptime(dt_leilao_obj, '%Y-%m-%d').date()
                    except ValueError:
                        dt_leilao_obj = None
                
                # Regra de negócio para definir a cor na tela
                l['status'] = 'Realizado' if dt_leilao_obj and dt_leilao_obj < hoje else 'Agendado'
                l['dt_leilao'] = dt_leilao_obj.strftime('%Y-%m-%d') if dt_leilao_obj else ''
                
                # Associa os animais da query ao leilão correto via Python
                l['animais'] = [a for a in animais_vinculados if a['id_leilao'] == l['id_leilao']]
                
        return JsonResponse(leiloes, safe=False)

    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO leilao (nome_evento, dt_leilao, custo_fixo, local) 
                    VALUES (%s, %s, %s, %s) RETURNING id_leilao
                """, [dados.get('nome_evento'), dados.get('dt_leilao'), dados.get('custo_fixo', 0), dados.get('local', '')])
                
                novo_leilao_id = cursor.fetchone()[0]
                
                # UPDATE usando operador ANY do PostgreSQL
                if 'animais_ids' in dados and len(dados['animais_ids']) > 0:
                    cursor.execute("""
                        UPDATE animal SET id_leilao = %s WHERE id_animal = ANY(%s)
                    """, [novo_leilao_id, dados['animais_ids']])
                    
            return JsonResponse({'sucesso': True, 'id_leilao': novo_leilao_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
def detalhe_leilao(request, id_leilao):
    if request.method == 'PUT':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE leilao 
                    SET nome_evento = COALESCE(%s, nome_evento),
                        dt_leilao = COALESCE(%s, dt_leilao),
                        custo_fixo = COALESCE(%s, custo_fixo),
                        local = COALESCE(%s, local)
                    WHERE id_leilao = %s
                """, [dados.get('nome_evento'), dados.get('dt_leilao'), dados.get('custo_fixo'), dados.get('local'), id_leilao])

                if 'animais_ids' in dados:
                    # Passo 1: Desvincula os animais antigos
                    cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_leilao = %s", [id_leilao])
                    # Passo 2: Vincula os novos selecionados nos checkboxes
                    if len(dados['animais_ids']) > 0:
                        cursor.execute("UPDATE animal SET id_leilao = %s WHERE id_animal = ANY(%s)", [id_leilao, dados['animais_ids']])

            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            # Desvincula animais antes de deletar o leilão para não violar a chave estrangeira
            cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_leilao = %s", [id_leilao])
            cursor.execute("DELETE FROM leilao WHERE id_leilao = %s", [id_leilao])
        return JsonResponse({'sucesso': True})