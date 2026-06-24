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
# Função para realizar o login do usuário
def realizar_login(request):
    if request.method == 'POST': # Verifica se o método da requisição é POST
        try:
            dados = json.loads(request.body)
            usuario_input = dados.get('email') # Obtém o valor do campo 'email' do corpo da requisição
            senha_input = dados.get('senha') # Obtém o valor do campo 'senha' do corpo da requisição
            
            with connection.cursor() as cursor: # Abre uma conexão com o banco de dados e cria um cursor para executar consultas SQL
                cursor.execute("""
                    SELECT nome, senha, perfil, usuario
                    FROM dono
                    WHERE usuario = %s
                """, [usuario_input])
                row = cursor.fetchone()

            if not row: # Verifica se o usuário não foi encontrado no banco de dados
                return JsonResponse({'sucesso': False, 'mensagem': 'Usuário não encontrado.'}, status=401)

            if row[1] != senha_input: # Verifica se a senha fornecida não corresponde à senha armazenada no banco de dados
                return JsonResponse({'sucesso': False, 'mensagem': 'Senha incorreta.'}, status=401)

            return JsonResponse({ # Retorna uma resposta JSON indicando sucesso no login, juntamente com informações do usuário
                'sucesso': True,
                'nome_usuario': row[0],
                'perfil': row[2] or 'Dono',
                'usuario': row[3]
            })

        except Exception as e:
            return JsonResponse({'sucesso': False, 'mensagem': f'Erro: {str(e)}'}, status=500)
    return JsonResponse({'sucesso': False, 'mensagem': 'Método inválido.'}, status=405)

# ------------------------- ANIMAIS -------------------------
@csrf_exempt
def gerenciar_animais(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id_animal as id, a.numero_brinco as nome, a.raca, a.status, a.sexo,
                       a.peso, a.dt_nasc, a.dt_morte, a.causa_morte,
                       d.nome as dono_nome, c.descricao as categoria_desc,
                       COALESCE(l.nome_evento, 'Não vinculado') as leilao_nome,
                       a.id_dono, a.id_categoria, a.id_leilao,
                       EXISTS(SELECT 1 FROM venda v WHERE v.id_animal = a.id_animal) as is_vendido,
                       EXISTS(
                           SELECT 1 FROM aplicacao ap 
                           INNER JOIN medicamento m ON ap.id_medicamento = m.id_medicamento 
                           WHERE ap.id_animal = a.id_animal AND m.tp_medicamento IN ('ANT', 'PAR')
                       ) as is_doente
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
                a['dt_morte'] = a['dt_morte'].strftime('%Y-%m-%d') if a.get('dt_morte') else ''
        return JsonResponse(animais, safe=False)

    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO animal (numero_brinco, raca, status, sexo, peso, dt_nasc, id_dono, id_categoria, causa_morte, dt_morte)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CASE WHEN %s = 'M' THEN CURRENT_DATE ELSE NULL END)
                    RETURNING id_animal
                """, [
                    dados.get('nome', ''), dados.get('raca', ''), dados['status'], dados['sexo'],
                    dados['peso'], dados.get('dt_nasc', '2024-01-01'), dados['id_dono'], dados['id_categoria'],
                    dados.get('causa_morte') if dados.get('status') == 'M' else None,
                    dados['status']
                ])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'id': novo_id, 'sucesso': True}, status=201)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

@csrf_exempt
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
                        causa_morte = %s,
                        dt_morte = CASE WHEN %s = 'M' THEN COALESCE(dt_morte, CURRENT_DATE) ELSE NULL END
                    WHERE id_animal = %s
                """, [
                    dados.get('nome'), dados.get('raca'), dados.get('status'), dados.get('sexo'),
                    dados.get('peso'), dados.get('id_dono'), dados.get('id_categoria'),
                    dados.get('causa_morte') if dados.get('status') == 'M' else None,
                    dados.get('status'),
                    id_animal
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
            cursor.execute("""SELECT id_categoria, descricao, nome_categoria 
                           FROM categoria 
                           ORDER BY id_categoria""")
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
def detalhe_categoria(request, id_categoria):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id_categoria, descricao, nome_categoria 
                           FROM categoria 
                           WHERE id_categoria = %s", [id_categoria]
                           """)
            row = cursor.fetchone()
            if not row:
                return JsonResponse({'erro': 'Categoria não encontrada'}, status=404)
            return JsonResponse({'id': row[0], 'descricao': row[1], 'nome_categoria': row[2]})
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
            cursor.execute("""DELETE FROM categoria 
                           WHERE id_categoria = %s", [id_categoria]
                           """)
        return JsonResponse({'sucesso': True})

# ------------------------- PROPRIETÁRIOS -------------------------
@csrf_exempt
def gerenciar_proprietarios(request):
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
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM dono WHERE id_dono = %s", [id_dono])
        return JsonResponse({'sucesso': True})
    
# ------------------------- LEILÕES -------------------------
@csrf_exempt
def gerenciar_leiloes(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_leilao, nome_evento, dt_leilao, custo_fixo, local
                FROM leilao
                ORDER BY dt_leilao
            """)
            leiloes = fetch_as_dict(cursor)
            cursor.execute("""
                SELECT id_animal as id, numero_brinco as nome, raca, id_leilao, peso, id_dono 
                FROM animal 
                WHERE id_leilao IS NOT NULL
            """)
            animais_vinculados = fetch_as_dict(cursor)
            hoje = date.today()

            for l in leiloes:
                l['custo_fixo'] = float(l['custo_fixo']) if l['custo_fixo'] is not None else 0.0
                dt_leilao_obj = l['dt_leilao']
                if isinstance(dt_leilao_obj, str):
                    try:
                        dt_leilao_obj = datetime.strptime(dt_leilao_obj, '%Y-%m-%d').date()
                    except ValueError:
                        dt_leilao_obj = None

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
                        l['extra_label'] = 'Possível Leilão'
                    else:
                        l['color_class'] = 'card-agendado-proximo'
                        l['status_text'] = 'Agendado'
                else:
                    l['color_class'] = 'card-agendado-proximo'
                    l['status_text'] = 'Hoje'

                l['dt_leilao'] = dt_leilao_obj.strftime('%Y-%m-%d') if dt_leilao_obj else ''
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
                if 'animais_ids' in dados and len(dados['animais_ids']) > 0:
                    cursor.execute("""
                        UPDATE animal
                        SET id_leilao = %s
                        WHERE id_animal = ANY(%s)
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
                    novos_animais = set(dados['animais_ids']) 
                    cursor.execute("""
                        SELECT id_animal
                        FROM animal
                        WHERE id_leilao = %s
                    """, [id_leilao])
                    animais_atuais = set(row[0] for row in cursor.fetchall())
                    animais_para_remover = list(animais_atuais - novos_animais) 
                    animais_para_adicionar = list(novos_animais - animais_atuais) 
                    
                    if animais_para_remover:
                        cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_animal = ANY(%s)", [animais_para_remover])
                    if animais_para_adicionar:
                        cursor.execute("UPDATE animal SET id_leilao = %s WHERE id_animal = ANY(%s)", [id_leilao, animais_para_adicionar])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
       
    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("UPDATE animal SET id_leilao = NULL WHERE id_leilao = %s", [id_leilao])
            cursor.execute("DELETE FROM leilao WHERE id_leilao = %s", [id_leilao])
        return JsonResponse({'sucesso': True})

@csrf_exempt
def info_detalhada_leilao(request, id_leilao):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT nome_evento, dt_leilao, local, custo_fixo FROM leilao WHERE id_leilao = %s", [id_leilao])
                leilao_info = cursor.fetchone()
                if not leilao_info:
                    return JsonResponse({'erro': 'Leilão não encontrado'}, status=404)

                data_leilao = leilao_info[1]
                hoje = date.today()
                status_text = 'Realizado' if data_leilao and data_leilao < hoje else 'Agendado'

                cursor.execute("""
                    SELECT COUNT(id_animal), SUM(peso), AVG(peso), COUNT(DISTINCT id_dono)
                    FROM animal
                    WHERE id_leilao = %s
                """, [id_leilao])
                metricas = cursor.fetchone()
                qtd_animais = metricas[0] or 0
                peso_total = float(metricas[1]) if metricas[1] else 0.0
                peso_medio = float(metricas[2]) if metricas[2] else 0.0
                qtd_proprietarios = metricas[3] or 0

                cursor.execute("""
                    SELECT c.descricao, COUNT(*) as total
                    FROM animal a
                    JOIN categoria c ON a.id_categoria = c.id_categoria
                    WHERE a.id_leilao = %s
                    GROUP BY c.id_categoria, c.descricao
                """, [id_leilao])
                categorias = fetch_as_dict(cursor)

                cursor.execute("""
                    SELECT d.nome, d.id_dono, COUNT(*) as total_animais
                    FROM animal a
                    JOIN dono d ON a.id_dono = d.id_dono
                    WHERE a.id_leilao = %s
                    GROUP BY d.id_dono, d.nome
                """, [id_leilao])
                proprietarios_dist = fetch_as_dict(cursor)

                for p in proprietarios_dist:
                    if qtd_animais > 0:
                        p['porcentagem'] = round((p['total_animais'] / qtd_animais) * 100, 1)
                    else:
                        p['porcentagem'] = 0

            return JsonResponse({
                'id_leilao': id_leilao,
                'nome_evento': leilao_info[0],
                'dt_leilao': leilao_info[1].strftime('%Y-%m-%d') if leilao_info[1] else '',
                'local': leilao_info[2],
                'custo_fixo': float(leilao_info[3]) if leilao_info[3] else 0.0,
                'status_text': status_text,
                'qtd_animais': qtd_animais,
                'peso_total': peso_total,
                'peso_medio': peso_medio,
                'qtd_proprietarios': qtd_proprietarios,
                'categorias': categorias,
                'distribuicao_proprietarios': proprietarios_dist
            })

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

# ------------------------- VENDAS -------------------------
@csrf_exempt
def gerenciar_vendas(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT v.id_venda, a.numero_brinco as animal_nome, v.dt_venda,
                       v.vendedor, v.comprador, v.vlr_venda as valor, v.tp_pgto as tipo_pagamento,
                       COALESCE(l.nome_evento, 'Venda Direta') as leilao_nome,
                       v.id_animal, v.id_leilao, v.justificativa_alteracao,
                       a.id_dono 
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
                cursor.execute("""
                    SELECT dt_leilao 
                    FROM leilao 
                    WHERE id_leilao = %s
                """, [id_leilao])
                row_leilao = cursor.fetchone()
                
                if not row_leilao:
                    return JsonResponse({'sucesso': False, 'erro': 'Leilão não encontrado no sistema.'}, status=400)
                
                dt_leilao = row_leilao[0]
                if isinstance(dt_leilao, str):
                    dt_leilao = datetime.strptime(dt_leilao, '%Y-%m-%d').date()
                    
                if dt_leilao > date.today():
                    return JsonResponse({
                        'sucesso': False, 
                        'erro': 'Apenas leilões já realizados (data no passado ou hoje) podem ser faturados em lote.'
                    }, status=400)

                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM venda 
                    WHERE id_leilao = %s
                """, [id_leilao])
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({
                        'sucesso': False, 
                        'erro': 'Este leilão já possui um faturamento registrado no sistema.'
                    }, status=400)

                cursor.execute("""
                    INSERT INTO venda (id_animal, vendedor, comprador, vlr_venda, dt_venda, tp_pgto, id_leilao)
                    SELECT id_animal, %s, %s, %s, %s, %s, id_leilao
                    FROM animal WHERE id_leilao = %s
                """, [
                    dados['vendedor'], dados['comprador'], dados['valor_padrao'],
                    dados['data_venda'], dados['tipo_pagamento'], id_leilao
                ])
                
                if cursor.rowcount == 0:
                    return JsonResponse({
                        'sucesso': False, 
                        'erro': 'Nenhum animal vinculado a este leilão foi encontrado para realizar o faturamento.'
                    }, status=400)

            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)


# ------------------------- MEDICAMENTOS E APLICAÇÕES -------------------------
@csrf_exempt
def gerenciar_medicamentos(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_medicamento, nome, tp_medicamento FROM medicamento ORDER BY nome")
            medicamentos = fetch_as_dict(cursor)
        return JsonResponse(medicamentos, safe=False)
    
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO medicamento (nome, tp_medicamento)
                    VALUES (%s, %s) RETURNING id_medicamento
                """, [dados.get('nome'), dados.get('tp_medicamento')])
                novo_id = cursor.fetchone()[0]
            return JsonResponse({'sucesso': True, 'id_medicamento': novo_id}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
def gerenciar_aplicacoes(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ap.id_animal, ap.id_medicamento, ap.dt_aplicacao, ap.lote, ap.informado_indea,
                       an.numero_brinco as animal_nome, an.id_dono, m.nome as medicamento_nome, m.tp_medicamento
                FROM aplicacao ap
                INNER JOIN animal an ON ap.id_animal = an.id_animal
                INNER JOIN medicamento m ON ap.id_medicamento = m.id_medicamento
                ORDER BY ap.dt_aplicacao DESC
            """)
            aplicacoes = fetch_as_dict(cursor)
            for ap in aplicacoes:
                dt = ap.get('dt_aplicacao') or ap.get('Dt_Aplicacao')
                if isinstance(dt, date):
                    ap['dt_aplicacao'] = dt.strftime('%Y-%m-%d')
                elif dt:
                    ap['dt_aplicacao'] = str(dt)
                else:
                    ap['dt_aplicacao'] = ''
        return JsonResponse(aplicacoes, safe=False)
    
    elif request.method == 'POST':
        try:
            dados = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM aplicacao 
                    WHERE id_animal = %s AND id_medicamento = %s
                """, [dados['id_animal'], dados['id_medicamento']])
                
                if cursor.fetchone()[0] > 0:
                    return JsonResponse({'sucesso': False, 'erro': 'Este animal já possui registro para este medicamento específico.'}, status=400)

                cursor.execute("""
                    INSERT INTO aplicacao (id_animal, id_medicamento, dt_aplicacao, lote, informado_indea)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    dados['id_animal'], dados['id_medicamento'], dados['dt_aplicacao'],
                    dados.get('lote', ''), dados.get('informado_indea', 'N')
                ])
            return JsonResponse({'sucesso': True}, status=201)
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)

@csrf_exempt
def detalhe_aplicacao(request, id_animal, id_medicamento):
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM aplicacao WHERE id_animal = %s AND id_medicamento = %s", [id_animal, id_medicamento])
            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)}, status=400)