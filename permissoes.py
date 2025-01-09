from functools import wraps
from flask import request, jsonify
from models import Usuario
from user import verificar_token

# Dicionário de permissões
permissoes_por_cargo = {
    'Admin': [
        'gerenciar_usuarios', 'visualizar_logs', 'acessar_tudo', 
        'aprovar_usuarios', 'criar_cargo', 'criar_permissao', 
        'editar_cargo', 'editar_permissao', 'deletar_cargo', 
        'deletar_permissao', 'criar_equipe', 'editar_equipe', 
        'deletar_equipe', 'criar_ranking', 'editar_ranking', 
        'deletar_ranking', 'criar_pontuacao', 'editar_pontuacao', 
        'deletar_pontuacao'
    ],
    'Gerente': [
        'visualizar_rankings', 'visualizar_historico', 
        'visualizar_equipes', 'listar_rankings', 
        'listar_equipes', 'listar_pontuacoes'
    ],
    'Corretor': [
        'visualizar_rankings', 'visualizar_pontuacoes', 
        'listar_rankings', 'listar_pontuacoes'
    ],
    'Assistente_de_Locacao': [
        'visualizar_rankings', 'visualizar_pontuacoes', 
        'listar_pontuacoes', 'listar_equipes'
    ],
    'Suporte': [
        'visualizar_usuarios', 'listar_usuarios'
    ]
}

def verificar_permissao(permissao_necessaria):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extrai o token de autorização do cabeçalho da requisição
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token não fornecido!'}), 401
            try:
                # Verifica e decodifica o token
                token = token.split(' ')[1] if ' ' in token else token
                user_id = verificar_token(token)
                if not user_id:
                    return jsonify({'error': 'Token inválido ou expirado'}), 401
                
                # Busca o usuário e o cargo dele no banco de dados
                usuario = Usuario.query.get(user_id)
                if not usuario:
                    return jsonify({'error': 'Usuário não encontrado!'}), 404
                
                # Verifica se o cargo do usuário possui a permissão necessária
                cargo = usuario.cargo
                permissoes_do_cargo = permissoes_por_cargo.get(cargo, [])
                if permissao_necessaria not in permissoes_do_cargo:
                    return jsonify({'error': f'Acesso negado! Cargo {cargo} não possui a permissão {permissao_necessaria}.'}), 403
            except Exception as e:
                return jsonify({'error': f'Erro na autenticação: {str(e)}'}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator