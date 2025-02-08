import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app, db
from models import Usuario, Cargo
from dotenv import load_dotenv
import os
import subprocess
import unicodedata

# Carrega as variáveis do .env
load_dotenv()

class TestRoutes(TestCase):

    def create_app(self):
        # Configurações de teste
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
        app.config['SECRET_ACCESS_KEY'] = os.getenv('SECRET_ACCESS_KEY')
        return app

    def setUp(self):
        # Cria as tabelas no banco de dados
        db.create_all()
        
        # Executa o seeds.py
        subprocess.run(['python', 'seeds.py'], check=True)
        
        # Executa o seeds_permissoes.py
        subprocess.run(['python', 'seeds_permissoes.py'], check=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def normalize_str(self, s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')

    def test_auto_cadastrar_admin(self):
        response = self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 201)
        self.assertIn('Usuário Josué foi adicionado com sucesso!', response.get_json().get('message'))

    def test_cadastrar_usuario(self):
        response = self.client.post('/api/cadastrar', json={
            'nome': 'Maria Eduarda',
            'email': 'mariaeduarda@gmail.com',
            'senha': 'senha123',
            'cargo': 'Gerente',
            'equipe': 'Conecta',
            'instagram': 'duddacunha'
        })
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 201)
        self.assertIn('Usuário Maria Eduarda foi adicionado com sucesso!', response.get_json().get('message'))

    def test_login(self):
        # Primeiro, faça o auto-cadastro do administrador para garantir que ele exista
        self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })

        # Faça o login com as credenciais do administrador
        response = self.client.post('/api/login', json={
            'email': 'josue@gmail.com',
            'senha': 'senha123'
        })
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_visualizar_perfil(self):
        # Primeiro, faça login para obter o token
        self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })
        login_response = self.client.post('/api/login', json={
            'email': 'josue@gmail.com',
            'senha': 'senha123'
        })
        token = login_response.json['token']

        # Visualize o perfil usando o token
        response = self.client.get('/api/perfil', headers={'Authorization': f'Bearer {token}'})
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 200)
        self.assertIn('Josué', response.get_json().get('nome'))

    def test_editar_perfil(self):
        # Primeiro, faça login para obter o token
        self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })
        login_response = self.client.post('/api/login', json={
            'email': 'josue@gmail.com',
            'senha': 'senha123'
        })
        token = login_response.json['token']

        # Agora, edite o perfil usando o token
        response = self.client.put('/api/perfil/editar', json={
            'nome': 'Josue Editado',
            'email': 'josue_editado@gmail.com',
            'instagram': 'josue_editadooficial'
        }, headers={'Authorization': f'Bearer {token}'})
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 200)
        self.assertIn('Perfil atualizado com sucesso!', response.get_json().get('message'))

    def test_redefinir_senha(self):
        self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })
        response = self.client.post('/api/redefinir_senha', json={
            'email': 'josue@gmail.com',
            'nova_senha': 'nova_senha123'
        })
        print(response.data)  # Log para depuração
        self.assertEqual(response.status_code, 200)
        self.assertIn('Senha redefinida com sucesso!', response.get_json().get('message'))

    def test_upload_imagem_perfil(self):
        self.client.post('/api/admin/cadastro', json={
            'access_key': current_app.config['SECRET_ACCESS_KEY'],
            'nome': 'Josué',
            'email': 'josue@gmail.com',
            'senha': 'senha123',
            'instagram': 'josueoficial'
        })
        login_response = self.client.post('/api/login', json={
            'email': 'josue@gmail.com',
            'senha': 'senha123'
        })
        token = login_response.json['token']

        # Verifique se o arquivo existe antes de tentar abri-lo
        file_path = 'tests/test_image.jpg'
        if not os.path.exists(file_path):
            self.skipTest(f"O arquivo {file_path} não existe.")

        # Faça o upload da imagem de perfil usando o token
        with open(file_path, 'rb') as img:
            response = self.client.post('/api/perfil/upload_imagem', content_type='multipart/form-data', data={
                'imagem': img
            }, headers={'Authorization': f'Bearer {token}'})
            print(response.data)  # Log para depuração
            self.assertEqual(response.status_code, 200)
            self.assertIn('imagem_url', response.get_json())

if __name__ == '__main__':
    unittest.main()
