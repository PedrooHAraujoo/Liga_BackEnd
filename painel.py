from flask import Blueprint, request, jsonify
from models import db
from crud import *
from permissoes import verificar_permissao # Decorador para verificar permissões
from user import *
painel_bp = Blueprint('painel', __name__)

# Endpoint do painel Administração
@painel_bp.route('/admin', methods=['GET'])
@verificar_permissao('acessar_tudo') # Aoebas administradores com a permisão 'acessar_tudo'
def painel_admin():
    return jsonify({
        'message': 'Bem vindo ao Painel de Administração!',
        'funções_disponíveis': [
            'Gerenciar Equipes',
            'Gerenciar Rankings',
            'Gerenciar Usuários',
            'Visualizar Logs',
            'Aprovar usuários',
            'Criar Cargo',
            'Criar Permissão',
            'Editar Cargo',
            'Editar Permissão',
            'Deletar Cargo',
            'Deletar Permissão',
            'Criar Pontuação',
            'Editar Pontuação',
            'Deletar Pontuação',
            'Visualizar Histórico',
            'Listar Equipes',
            'Listar Rankings',
            'Listar Pontuações',
            'Visualizar Pontuações',
            'Listar Usuários',
            'Visualizar Usuários'
        ]
    }), 200
# Endpoints para Equipe
@painel_bp.route('/equipe', methods=['POST'])
@verificar_permissao('gerenciar_equipes') # Apenas os usuários com a permissão 'gerenciar_equipes' pode acessar
def criar_nova_equipe():
    data = request.json
    nome = data.get('nome')
    tipo = data.get('tipo')

    if not nome:
        return jsonify({
            'Status': 'Error',
            'Message': 'O nome da equipe é obrigatório!'
        }), 400
    if not tipo:
        return jsonify({
            'Status': 'Error',
            'Message': 'O tipo da equipe é obrigatório!'
        }), 400
    equipe = criar_equipe(nome, tipo)
    return jsonify({
        'id': equipe.id, 
        'nome': equipe.nome,
        'tipo': equipe.tipo
    }), 201

@painel_bp.route('/equipe', methods=['GET'])
@verificar_permissao('visualizar_equipes') # Apenas os usuários com a permissão 'visualizar_equipes' pode acessar
def listar_todas_equipes():
    equipes = listar_equipes()
    return jsonify([{
        'id': e.id,
        'nome': e.nome,
        'tipo': e.tipo
    } for e in equipes]), 200

@painel_bp.route('/equipe/<int:id>', methods=['PUT'])
@verificar_permissao('gerenciar_equipes') # Apenas os usuários com a permissão 'gerenciar_equipes' pode acessar
def atualizar_uma_equipe(id):
    data = request.json
    nome = data.get('nome')
    tipo = data.get('tipo')

    equipe = atualizar_equipe(id, nome=nome, tipo=tipo)
    if not equipe:
        return jsonify({
            'Status': 'Error',
            'Message': 'Equipe não encontrada!'
        }), 404
    return jsonify({
        'id': equipe.id,
        'nome': equipe.nome,
        'tipo': equipe.tipo
    }), 200

@painel_bp.route('/equipe/<int:id>', methods=['DELETE'])
@verificar_permissao('gerenciar_equipes') # Apenas os usuários com a permissão 'gerenciar_equipes' pode acessar
def deletar_uma_equipe(id):
    if deletar_equipe(id):
        return jsonify({
            'Status':'Success',
            'Message': 'Equipe deletada com sucesso!'
        }), 200
    return jsonify({
        'Status': 'Error',
        'Message': 'Equipe não encontrada!'
    }), 404

# Endpoints para Ranking
@painel_bp.route('/ranking', methods=['POST'])
@verificar_permissao('gerenciar_rankings') # Apenas os usuários com a permissão 'gerenciar_rankings' pode acessar
def criar_novo_ranking():
    data = request.json
    nome_ranking = data.get('nome_ranking')
    meta_pontuacao = data.get('meta_pontuacao')
    
    if not nome_ranking:
        return jsonify({
            'Status': 'Error',
            'Message': 'O nome do ranking é obrigatório.'
        }), 400
    
    ranking = criar_ranking(nome_ranking=nome_ranking, meta_pontuacao=meta_pontuacao)
    return jsonify({
        'id': ranking.id,
        'nome_ranking': ranking.nome_ranking,
        'meta_pontuacao': ranking.meta_pontuacao

    }), 201

@painel_bp.route('/ranking', methods=['GET'])
@verificar_permissao('visualizar_rankings') # Apenas os usuários com a permissão 'visualizar_rankings' pode acessar
def listar_todos_rankings():
    rankings = listar_ranking()
    return jsonify([{
        'id': r.id,
        'nome_ranking': r.nome_ranking,
        'meta_pontuacao': r.meta_pontuacao
    } for r in rankings]), 200

@painel_bp.route('/ranking/<int:id>', methods=['PUT'])
@verificar_permissao('gerenciar_rankings') # Apenas os usuários com a permissão 'gerenciar_rankings' pode acessar
def atualizar_tipo_ranking(id):
    data = request.json
    nome_ranking = data.get('nome_ranking')
    meta_pontuacao = data.get('meta_pontuacao')

    ranking = atualizar_ranking(id, nome_ranking=nome_ranking, meta_pontuacao=meta_pontuacao)
    if not ranking:
        return jsonify({
            'Status': 'Error',
            'Message': 'Ranking não encontrado.'
        }), 404
    return jsonify({
        'id': ranking.id,
        'nome_ranking': ranking.nome_ranking,
        'meta_pontuacao': ranking.meta_pontuacao        
    }), 200

@painel_bp.route('/ranking/<int:id>', methods=['DELETE'])
@verificar_permissao('gerenciar_rankings') # Apenas os usuários com a permissão 'gerenciar_rankings' pode acessar
def deletar_um_ranking(id):
    if deletar_ranking(id):
        return jsonify({
            'Status': 'success',
            'Message': 'Deletado com sucesso!'
        }), 200
    return jsonify({
        'Status': 'Error',
        'Message': 'Ranking não encontrado"'
    }), 404

# Endpoints para Gerenciamento de Usuários com Status de Aprovação
@painel_bp.route('/usuario/<int:id>/aprovar', methods=['PUT'])
@verificar_permissao('gerenciar_usuarios')
def aprovar_usuario(id):
    usuario = atualizar_usuario(id, status='aprovado')
    if not usuario:
        return jsonify({
            'Status': 'Error',
            'Message': 'Usuário não encontrado.'
        }), 404
    return jsonify({
        'Status': usuario.status,
        'Message': f'Usuário {usuario.nome} aprovado com sucesso.'
    }), 200

@painel_bp.route('/usuario/<int:id>', methods=['PUT'])
@verificar_permissao('gerenciar_usuarios')
def atualizar_dados_usuario(id):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    instagram = data.get('instagram')

    response, status_code = atualizar_usuario(id, nome, email, instagram)
    return jsonify(response), status_code

@painel_bp.route('/usuario/<int:id>', methods=['GET'])
@verificar_permissao('visualizar_usuarios')
def obter_usuario_por_id(id):
    response, status_code = obter_usuario(id)
    return jsonify(response), status_code

@painel_bp.route('/usuario/<int:id>', methods=['DELETE'])
@verificar_permissao('gerenciar_usuarios')
def deletar_usuario(id):
    if deletar_usuario_crud(id):
        return jsonify({
            'Status': 'Success',
            'Message': 'Usuário deletado com sucesso'
        }), 200
    return jsonify({
        'Status': 'Error',
        'Message': 'Usuário não encontrado'
    }), 404

# Endpoints para Pontuação 
#@painel_bp.route('/pontuacao', methods=['POST'])
#@verificar_permissao('gerenciar_pontuacoes')  # Apenas os usuários com a permissão 'gerenciar_pontuacoes' pode acessar
#def criar_pontuacao():
