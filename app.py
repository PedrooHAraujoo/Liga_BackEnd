from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from user import adicionar_usuario, login_usuario, redefinir_senha, verificar_token
from dotenv import load_dotenv
import os
import jwt
from functools import wraps

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados a partir do .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # Chave secreta JWT

# Inicializa o SQLAlchemy com o app
db.init_app(app)

def jwt_required(f):
    @wraps(f) # Decorador do Python que preserva as informações originais da função decorada
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token não fornecido!'}), 401
        try:
            # Extrai o token do header Authorization
            token = token.split('')[1]if '' in token else token
            user_id = verificar_token(token)
            if not user_id:
                return jsonify({'error': 'Token inválido ou expirado!'}), 401
        except Exception as e:
            return jsonify({'error': f'Erro na autenticação: {str(e)}'}), 401
        return f(user_id, *args, **kwargs)
    return decorated_function
# Rota para cadastro de usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    cargo = data.get('cargo')
    equipe = data.get('equipe')
    instagram = data.get('instagram')

    
    if not nome or not email or not senha or not cargo or not equipe or not instagram:
        return jsonify({'error': 'Preencha todos os campos!'}), 400


    resultado, status_code = adicionar_usuario(nome, email, senha, cargo, equipe, instagram)
    return jsonify(resultado), status_code
# Rota para redefinir a senha
@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha_endpoint():
    data = request.json
    email = data.get('email')
    nova_senha = data.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({'error': 'Preencha o email e a nova senha!'}), 400
    
    resposta, status = redefinir_senha(email, nova_senha)
    return jsonify(resposta), status

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'error': 'Preencha email e a senha!'}), 400
    resposta, status = login_usuario(email, senha)
    return jsonify(resposta), status

# Criação do banco de dados com as tabelas
with app.app_context():                
    db.create_all() # Cria as tabelas no banco de dados
    
if __name__ == '__main__':
    app.run(debug=True)
