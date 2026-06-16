import json
from datetime import date, datetime
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

def fetch_as_dict(cursor):
    """Converte o resultado do cursor em lista de dicionários."""
    colunas = [col[0] for col in cursor.description]
    return [dict(zip(colunas, row)) for row in cursor.fetchall()]

# ------------------------- LOGIN -------------------------
@csrf_exempt
def realizar_login(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            usuario_input = dados.get('email')
            senha_input = dados.get('senha')

        
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT nome, senha, perfil, usuario
                    FROM dono
                    WHERE usuario = %s
                """, [usuario_input])
                row = cursor.fetchone()

            if not row:
                return JsonResponse({'sucesso': False, 'mensagem': 'Usuário não encontrado.'}, status=401)

            if row[1] != senha_input:
                return JsonResponse({'sucesso': False, 'mensagem': 'Senha incorreta.'}, status=401)

            return JsonResponse({
                'sucesso': True,
                'nome_usuario': row[0],
                'perfil': row[2] or 'Dono',
                'usuario': row[3]
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'mensagem': f'Erro: {str(e)}'}, status=500)
    return JsonResponse({'sucesso': False, 'mensagem': 'Método inválido.'}, status=405)

# ------------------------- PROPRIETÁRIOS -------------------------
@csrf_exempt
def gerenciar_proprietarios(request):
    # Gerencia a listagem e criação de proprietários (donos)
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT d.id_dono, d.nome, d.usuario, d.telefone, d.status_dono,
                       d.cor_brinco, d.descricao_marca, d.perfil,
                       (SELECT COUNT(*) FROM animal a WHERE a.id_dono = d.id_dono) as total_animais
                FROM dono d
                ORDER BY d.nome
            """)
            donos = fetch_as_dict(cursor)
            for d in donos:
                d['telefone'] = d['telefone'] or 'Não informado'
                d['descricao_marca'] = d['descricao_marca'] or 'Sem marca'
                d['perfil'] = d['perfil'] or 'Dono'
        return JsonResponse(donos, safe=False)

    elif request.method == 'POST':
        # Gerencia a criação de um novo proprietário (dono)
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO dono (nome, usuario, senha, status_dono, telefone, cor_brinco, descricao_marca, perfil)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_dono
                """, [
                    dados.get('nome'), dados.get('usuario'), dados.get('senha', '123456'),
                    dados.get('status_dono', 'A'), dados.get('telefone', ''),
                    dados.get('cor_brinco', ''), dados.get('descricao_marca', ''), dados.get('perfil', 'Dono')
                ])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'sucesso': True, 'id_dono': novo_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
# Gerencia a atualização e exclusão de um proprietário (dono) específico
def detalhe_proprietario(request, id_dono):
    if request.method == 'PUT':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
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
                if 'senha' in dados and dados['senha'].strip() != '':
                    cursor.execute("UPDATE dono SET senha = %s WHERE id_dono = %s", [dados['senha'], id_dono])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        # Antes de excluir o dono, desvincula os animais associados a ele
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM dono WHERE id_dono = %s", [id_dono])
        return JsonResponse({'sucesso': True})

# ------------------------- ANIMAIS -------------------------
@csrf_exempt
# Gerencia a listagem e criação de animais, incluindo detalhes como dono, categoria e leilão associado
def gerenciar_animais(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id_animal as id, a.numero_brinco as nome, a.raca, a.status, a.sexo,
                       a.peso, a.dt_nasc, a.causa_morte,
                       d.nome as dono_nome, c.descricao as categoria_desc,
                       COALESCE(l.nome_evento, 'Não vinculado') as leilao_nome,
                       a.id_dono, a.id_categoria, a.id_leilao
                FROM animal a
                LEFT JOIN dono d ON a.id_dono = d.id_dono
                LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
                LEFT JOIN leilao l ON a.id_leilao = l.id_leilao
                ORDER BY d.nome ASC
            """)
            animais = fetch_as_dict(cursor)
            for a in animais:
                a['peso'] = float(a['peso']) if a['peso'] else 0.0
                a['dt_nasc'] = a['dt_nasc'].strftime('%Y-%m-%d') if a['dt_nasc'] else ''
        return JsonResponse(animais, safe=False)

# Gerencia a criação de um novo animal, incluindo validações para campos obrigatórios e tratamento de dados relacionados a dono, categoria e leilão
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO animal (numero_brinco, raca, status, sexo, peso, dt_nasc, id_dono, id_categoria, causa_morte)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_animal
                """, [
                    dados.get('nome', ''), dados.get('raca', ''), dados['status'], dados['sexo'],
                    dados['peso'], dados.get('dt_nasc', '2024-01-01'), dados['id_dono'], dados['id_categoria'],
                    dados.get('causa_morte') if dados.get('status') == 'M' else None
                ])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'id': novo_id, 'sucesso': True}, status=201)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

@csrf_exempt
# Gerencia a atualização e exclusão de um animal específico, incluindo validações para campos obrigatórios e tratamento de dados relacionados a dono, categoria e leilão
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
                        id_categoria = COALESCE(%s, id_categoria),
                        causa_morte = %s
                    WHERE id_animal = %s
                """, [
                    dados.get('nome'), dados.get('raca'), dados.get('status'), dados.get('sexo'),
                    dados.get('peso'), dados.get('id_dono'), dados.get('id_categoria'),
                    dados.get('causa_morte') if dados.get('status') == 'M' else None,
                    id_animal
                ])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        # Antes de excluir o animal, desvincula-o de qualquer leilão associado
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM animal WHERE id_animal = %s", [id_animal])
        return JsonResponse({'sucesso': True})

# ------------------------- CATEGORIAS -------------------------
@csrf_exempt
def gerenciar_categorias(request):
    # Gerencia a listagem e criação de categorias, incluindo detalhes como descrição e nome da categoria
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
# Gerencia a atualização e exclusão de uma categoria específica, incluindo validações para campos obrigatórios e tratamento de dados relacionados a animais vinculados à categoria
def detalhe_categoria(request, id_categoria):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_categoria, descricao, nome_categoria FROM categoria WHERE id_categoria = %s", [id_categoria])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({'erro': 'Categoria não encontrada'}, status=404)
            return JsonResponse({'id': row[0], 'descricao': row[1], 'nome_categoria': row[2]})
    elif request.method == 'PUT':
        try:
            # Atualiza os detalhes de uma categoria específica, permitindo a modificação da descrição e do nome da categoria, com tratamento de dados para garantir a integridade das informações
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
        
    # Antes de excluir a categoria, desvincula os animais associados a ela, definindo o id_categoria como NULL    
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", [id_categoria])
        return JsonResponse({'sucesso': True})

# ------------------------- LEILÕES -------------------------
@csrf_exempt
# Gerencia a listagem e criação de leilões, incluindo detalhes como nome do evento, data, custo fixo, local e animais vinculados ao leilão, com tratamento de dados para exibir o status do leilão com base na data atual e para garantir a integridade das informações relacionadas aos animais vinculados ao leilão
def gerenciar_leiloes(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_leilao, nome_evento, dt_leilao, custo_fixo, local FROM leilao ORDER BY dt_leilao")
            leiloes = fetch_as_dict(cursor)
            cursor.execute("SELECT id_animal as id, numero_brinco as nome, raca, id_leilao FROM animal WHERE id_leilao IS NOT NULL")
            animais_vinculados = fetch_as_dict(cursor)
            hoje = date.today()

            # Para cada leilão, determina o status com base na data do leilão em relação à data atual, atribuindo classes de cor e textos de status apropriados para indicar se o leilão é realizado, agendado para o futuro ou se ocorreu recentemente, além de vincular os animais associados a cada leilão para exibição detalhada
            for l in leiloes:
                l['custo_fixo'] = float(l['custo_fixo']) if l['custo_fixo'] is not None else 0.0
                dt_leilao_obj = l['dt_leilao']
                if isinstance(dt_leilao_obj, str):
                    try:
                        # Converte a string de data para um objeto date, tratando possíveis erros de formatação
                        dt_leilao_obj = datetime.strptime(dt_leilao_obj, '%Y-%m-%d').date()
                    except ValueError:
                        dt_leilao_obj = None

                # Determina o status do leilão com base na data, atribuindo classes de cor e textos de status para indicar se o leilão é realizado, agendado para o futuro ou se ocorreu recentemente, considerando um período de 45 dias para diferenciar entre leilões recentes e antigos
                if dt_leilao_obj and dt_leilao_obj < hoje:
                    dias_atraso = (hoje - dt_leilao_obj).days
                    if dias_atraso > 45:
                        l['color_class'] = 'card-realizado-antigo'
                        l['status_text'] = 'Realizado (+45 dias)'
                    else:
                        l['color_class'] = 'card-realizado'
                        l['status_text'] = 'Realizado'
                elif dt_leilao_obj and dt_leilao_obj > hoje:
                    dias_futuro = (dt_leilao_obj - hoje).days
                    if dias_futuro > 45:
                        l['color_class'] = 'card-agendado-futuro'
                        l['status_text'] = 'Possível Leilão'
                        l['extra_label'] = '📅 Possível Leilão'
                    else:
                        l['color_class'] = 'card-agendado-proximo'
                        l['status_text'] = 'Agendado'
                else:
                    l['color_class'] = 'card-agendado-proximo'
                    l['status_text'] = 'Hoje'

                l['dt_leilao'] = dt_leilao_obj.strftime('%Y-%m-%d') if dt_leilao_obj else ''
                l['animais'] = [a for a in animais_vinculados if a['id_leilao'] == l['id_leilao']]

        return JsonResponse(leiloes, safe=False)

    # Gerencia a criação de um novo leilão, incluindo validações para campos obrigatórios e tratamento de dados relacionados aos animais vinculados ao leilão, garantindo a integridade das informações e a associação correta dos animais ao leilão criado
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO leilao (nome_evento, dt_leilao, custo_fixo, local)
                    VALUES (%s, %s, %s, %s) RETURNING id_leilao
                """, [dados.get('nome_evento'), dados.get('dt_leilao'), dados.get('custo_fixo', 0), dados.get('local', '')])
                novo_leilao_id = cursor.fetchone()[0]
                if 'animais_ids' in dados and len(dados['animais_ids']) > 0:
                    cursor.execute("UPDATE animal SET id_leilao = %s WHERE id_animal = ANY(%s)", [novo_leilao_id, dados['animais_ids']])
            return JsonResponse({'sucesso': True, 'id_leilao': novo_leilao_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
# Gerencia a atualização e exclusão de um leilão específico, incluindo validações para campos obrigatórios e tratamento de dados relacionados aos animais vinculados ao leilão, garantindo a integridade das informações e a associação correta dos animais ao leilão atualizado ou excluído, além de garantir que os animais sejam desvinculados do leilão caso este seja excluído, para manter a consistência dos dados no sistema
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
                    cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_leilao = %s", [id_leilao])
                    if len(dados['animais_ids']) > 0:
                        cursor.execute("UPDATE animal SET id_leilao = %s WHERE id_animal = ANY(%s)", [id_leilao, dados['animais_ids']])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_leilao = %s", [id_leilao])
            cursor.execute("DELETE FROM leilao WHERE id_leilao = %s", [id_leilao])
        return JsonResponse({'sucesso': True})

# ------------------------- VENDAS -------------------------
@csrf_exempt
# Gerencia a listagem e criação de vendas, incluindo detalhes como animal vendido, data da venda, vendedor, comprador, valor da venda, tipo de pagamento e leilão associado, com tratamento de dados para exibir as informações de forma clara e garantir a integridade das informações relacionadas às vendas registradas no sistema
def gerenciar_vendas(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT v.id_venda, a.numero_brinco as animal_nome, v.dt_venda,
                       v.vendedor, v.comprador, v.vlr_venda as valor, v.tp_pgto as tipo_pagamento,
                       COALESCE(l.nome_evento, 'Venda Direta') as leilao_nome,
                       v.id_animal, v.id_leilao, v.justificativa_alteracao
                FROM venda v
                INNER JOIN animal a ON v.id_animal = a.id_animal
                LEFT JOIN leilao l ON v.id_leilao = l.id_leilao
                ORDER BY v.dt_venda DESC
            """)
            vendas = fetch_as_dict(cursor)
            for v in vendas:
                v['valor'] = float(v['valor']) if v['valor'] else 0.0
                v['dt_venda'] = v['dt_venda'].strftime('%Y-%m-%d') if v['dt_venda'] else ''
        return JsonResponse(vendas, safe=False)

    elif request.method == 'POST':
        # Gerencia a criação de uma nova venda, incluindo validações para campos obrigatórios e tratamento de dados relacionados ao animal vendido, vendedor, comprador, valor da venda, tipo de pagamento e leilão associado, garantindo a integridade das informações e a associação correta dos dados relacionados à venda registrada no sistema
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO venda (id_animal, vendedor, comprador, vlr_venda, dt_venda, tp_pgto, id_leilao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_venda
                """, [
                    dados['id_animal'], dados.get('vendedor'), dados.get('comprador'),
                    dados['valor'], dados['data_venda'], dados['tipo_pagamento'], dados.get('id_leilao')
                ])
                nova_venda_id = cursor.fetchone()[0]
            return JsonResponse({'sucesso': True, 'id_venda': nova_venda_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
# Gerencia a atualização e exclusão de uma venda específica, incluindo validações para campos obrigatórios e tratamento de dados relacionados ao animal vendido, vendedor, comprador, valor da venda, tipo de pagamento e leilão associado, garantindo a integridade das informações e a associação correta dos dados relacionados à venda atualizada ou excluída no sistema, além de exigir uma justificativa para alterações em vendas existentes para manter um histórico claro das modificações realizadas, e restringir a exclusão de vendas apenas para usuários com perfil de administrador para garantir a segurança e a integridade dos dados relacionados às vendas registradas no sistema
def detalhe_venda(request, id_venda):
    if request.method == 'PUT':
        try:
            dados = json.loads(request.body)
            justificativa = dados.get('justificativa_alteracao', '').strip()
            if not justificativa:
                return JsonResponse({'sucesso': False, 'erro': 'A justificativa é obrigatória para alterar uma venda.'}, status=400)
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE venda
                    SET id_animal = %s, vendedor = %s, comprador = %s,
                        vlr_venda = %s, dt_venda = %s, tp_pgto = %s,
                        id_leilao = %s, justificativa_alteracao = %s
                    WHERE id_venda = %s
                """, [
                    dados['id_animal'], dados.get('vendedor'), dados.get('comprador'),
                    dados['valor'], dados['data_venda'], dados['tipo_pagamento'],
                    dados.get('id_leilao'), justificativa, id_venda
                ])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            perfil = request.GET.get('perfil', '')
            if perfil != 'Administrador':
                return JsonResponse({'sucesso': False, 'erro': 'Acesso negado. Apenas administradores podem excluir vendas.'}, status=403)
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM venda WHERE id_venda = %s", [id_venda])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
def importar_vendas_leilao(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            id_leilao = dados.get('id_leilao')
            
            with connection.cursor() as cursor:
                # 1. VALIDAÇÃO DE DATA (Só permite leilões do passado)
                cursor.execute("SELECT dt_leilao FROM leilao WHERE id_leilao = %s", [id_leilao])
                row_leilao = cursor.fetchone()
                
                if not row_leilao:
                    return JsonResponse({'sucesso': False, 'erro': 'Leilão não encontrado no sistema.'}, status=400)
                
                dt_leilao = row_leilao[0]
                if isinstance(dt_leilao, str):
                    dt_leilao = datetime.strptime(dt_leilao, '%Y-%m-%d').date()
                    
                if dt_leilao >= date.today():
                    return JsonResponse({
                        'sucesso': False, 
                        'erro': 'Apenas leilões já realizados (data no passado) podem ser faturados em lote.'
                    }, status=400)

                # 2. VALIDAÇÃO DE DUPLICIDADE (Não fatura o mesmo leilão duas vezes)
                cursor.execute("SELECT COUNT(*) FROM venda WHERE id_leilao = %s", [id_leilao])
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({
                        'sucesso': False, 
                        'erro': 'Este leilão já possui um faturamento registrado no sistema.'
                    }, status=400)

                # 3. EXECUÇÃO DO FATURAMENTO
                cursor.execute("""
                    INSERT INTO venda (id_animal, vendedor, comprador, vlr_venda, dt_venda, tp_pgto, id_leilao)
                    SELECT id_animal, %s, %s, %s, %s, %s, id_leilao
                    FROM animal WHERE id_leilao = %s
                """, [
                    dados['vendedor'], dados['comprador'], dados['valor_padrao'],
                    dados['data_venda'], dados['tipo_pagamento'], id_leilao
                ])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)