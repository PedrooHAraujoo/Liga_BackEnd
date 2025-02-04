import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Usuario
from user import (
    adicionar_usuario, login_usuario, redefinir_senha, verificar_token, 
    atualizar_usuario, salvar_imagem_perfil
)

# Inicializa o Blueprint para as rotas
app_routes = Blueprint('app_routes', __name__)

# Decorador para verificar o JWT
def verificar_jwt(f):
    @wraps(f)
    def decorated_functions(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token não fornecido!'}), 401
        try:
            token = token.split(' ')[1] if ' ' in token else token
            user_id = verificar_token(token)
            if not user_id:
                return jsonify({'error': 'Token inválido ou expirado'}), 401
        except Exception as e:
            return jsonify({'error': f'Erro na autenticação: {str(e)}'}), 401
        return f(user_id, *args, **kwargs)
    return decorated_functions

# Rota para cadastro de usuário
@app_routes.route('/cadastrar', methods=['POST'])
def cadastar():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    cargo = data.get('cargo')
    equipe = data.get('equipe')
    instagram = data.get('instagram')

    print(f"Dados recebidos: nome={nome}, email={email}, senha={senha}, cargo={cargo}, equipe={equipe}, instagram={instagram}")

    if not nome or not email or not senha or not cargo or not equipe or not instagram:
        return jsonify({'error': 'Preencha todos os campos!'}), 400
    
    resultado, status_code = adicionar_usuario(nome, email, senha, cargo, equipe, instagram)
    print(f"Resultado da adição: {resultado}")
    return jsonify(resultado), status_code

# Rota para redefinir a senha
@app_routes.route('/redefinir_senha', methods=['POST'])
def redefini_senha_endpoint():
    data = request.json
    email = data.get('email')
    nova_senha = data.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({'error': 'Preencha o email e a nova senha!'}), 400
    reposta, status = redefinir_senha(email, nova_senha)
    return jsonify(reposta), status

# Rota de Login
@app_routes.route("/login", methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'error': 'Preencha o email e a senha!'}), 400
    reposta, status = login_usuario(email, senha)
    return jsonify(reposta), status

# Rota para o perfil do usuario
@app_routes.route('/perfil', methods=['GET'])
@verificar_jwt
def visualizar_perfil(user_id):
    try:
        # Busca o usuário no banco de dados
        usuario = Usuario.query.get(user_id)

        if not usuario:
            return jsonify({
                'error': 'Usuario não encontrado',
                'status': 'fail'
            }), 404
        
        # Verifica se o atributo imagem_perfil existe e não é None
        if hasattr(usuario, 'imagem_perfil') and usuario.imagem_perfil:
            imagem_url = f"{request.host_url}uploads/{os.path.basename(usuario.imagem_perfil)}"
        else:
            imagem_url = None    

        # Retorna o perfil do usuario como JSON
        perfil_dict = usuario.to_dict()
        perfil_dict['imagem_perfil'] = imagem_url

        return jsonify(perfil_dict), 200
            
    except Exception as e:
        # Loga e retorna o erro
        print(f"Erro ao acessar perfil: {e}")
        return jsonify({
            "erro": "Erro ao acessar perfil",
            "status": "fail"
        }), 500

# Rota para editar o perfil 
@app_routes.route('/perfil/editar', methods=['PUT'])
@verificar_jwt
def editar_perfil(user_id):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    instagram = data.get('instagram')
    resultado, status_code = atualizar_usuario(user_id, nome, email, instagram)
    return jsonify(resultado), status_code

# Rota para upload de imagem de perfil
@app_routes.route('/perfil/upload_imagem', methods=['POST'])
@verificar_jwt
def upload_imagem(user_id):
    if 'imagem' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'Nenhuma imagem foi enviada'
        }), 400
    imagem = request.files['imagem']
    if imagem.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'Nome do arquivo inválido'
        }), 400
    
    # Usa a configuração do UPLOAD_FOLDER do app principal
    upload_folder = current_app.config['UPLOAD_FOLDER']
    resultado, status = salvar_imagem_perfil(user_id, imagem, upload_folder)

    # Retorna a URl acessível, se o upload for bem sucedido
    if status == 200:
        resultado['imagem_url'] = f"/api/uploads/{os.path.basename(resultado['imagem_url'])}"
    return jsonify(resultado), status

# Rota para servir imagens
@app_routes.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)