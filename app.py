from flask import Flask
from dotenv import load_dotenv
import os
from models import db
from routes import app_routes # Importando o Blueprint

# Carrega as variáveis de ambiente no arquivo .env
load_dotenv()

# Inicializa o app Flask
app = Flask(__name__)

# Configurações de banco de dados e chave do JWT
app.config['SQLALCHEMY_DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config('UPLOAD_FOLDER') = os.getenv('UPLOAD_FOLDER')
app.register_blueprint(app_routes, url_prefix='/api') # Registrando o Blueprint

# Inicializa o SQLALCHEMY com o app
db.init_app(app)

# Registra o Blueprint das rotas
app.register_blueprint(app_routes)

# Cria as tabelas no banco de dados 
with app.app_context():
    db.create_all()

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
