from flask import Flask
from dotenv import load_dotenv
import os
from models import db
from routes import app_routes  # Importando o Blueprint

# Função para criar e configurar o app
def create_app():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Inicializa o app Flask
    app = Flask(__name__)

    # Configurações de banco de dados e chave do JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Ajuste da URL do banco
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    # Registra o Blueprint das rotas
    app.register_blueprint(app_routes, url_prefix='/api')

    # Cria as tabelas no banco de dados
    with app.app_context():
        db.create_all()

    return app

# Se o arquivo for executado diretamente, o servidor Flask será iniciado
if __name__ == '__main__':
    app = create_app()  # Cria a aplicação Flask
    app.run(debug=True)
