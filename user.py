import bcrypt
import jwt
import datetime
from flask import current_app
from models import db, Usuario, Cargo, Equipe
from werkzeug.utils import secure_filename
import os

def adicionar_usuario(nome, email, senha, cargo, equipe, instagram):
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
       # Verifica se o email já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return {'error': 'O email já foi registrado.', 'status': 'fail'}, 400
       
        # Verifica se o cargo e equipe são válidos
        cargo_existente = Cargo.query.filter_by(nome=cargo).first()
        equipe_existente = Equipe.query.filter_by(nome=equipe).first()
        if not cargo_existente or not equipe_existente:
         return {'error': f'Cargo ou equipe inválidos: {cargo}, {equipe}', 'status': 'fail'}, 400

       
       # Se o email não existe cria um novo usuário
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hashed,
            cargo=cargo_existente, # Associa a instância de Cargo
            equipe=equipe_existente, # Associa a instância de Equipe
            instagram=instagram
        )
        
        db.session.add(novo_usuario) # Adiciona à sessão
        db.session.commit() # Confirma a transação
        return {'message': f'Usuário {nome} foi adicionado com sucesso!', 'status': 'success'}, 201
    
    except Exception as e:
        db.session.rollback() # Reverte a transação se houver erro
        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500
    
def redefinir_senha(email, nova_senha):

    senha_hashed = bcrypt.hashpw(nova_senha.encode('UTF-8'), bcrypt.gensalt())

    try:
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if not usuario_existente:
            return{'error': 'Usuário não encontrado', "status" : 'fail'}, 404
        
        # Atualiza a senha do usuário
        usuario_existente.senha = senha_hashed
        db.session.commit()

        return{'message' : 'Senha redefinida com sucesso!', 'status': 'sucess'},200
    
    except Exception as e:

        db.session.rollback() # Reverte a transação 

        return{'error' : f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500   

def login_usuario(email, senha):
    try:
        # Consulta o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário foi encontrado
        if not usuario:
            return{'error': 'Usuário não encontrado', 'status': 'fail'}, 404
        
        # Verifica se a senha foi fornecida corresponde à senha armazenada
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha):
            token = gerar_token(usuario.id)
            return{'token': token, 'status': 'success'}, 200
        else:
            return{'error': 'Credencias inválidas', 'status': 'fail'}, 401
    except Exception as e:
        return{"error": f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500

def gerar_token(user_id):
    payload ={
        'sub': str(user_id),
        'iat': datetime.datetime.utcnow(), # Registra o hor[ario em que o token foi gerado
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) # Token expira em 1 hora
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'),'HS256')
    return token

def verificar_token(token):
    try:
        print(f"Token completo: {token}")
        decoded = jwt.decode(
            token, 
            os.getenv('SECRET_KEY'), 
            algorithms=['HS256'],
        )
        
        return int(decoded.get('sub')) # Retorna o id do usuário
    
    except jwt.ExpiredSignatureError:
        print("Token expirado") 
        return None
    except jwt.InvalidTokenError as e:
        print(f"Erro de token: {type(e)} - {e}")
        return None


def obter_usuario(user_id):
    try:
        # Consulta o usuário pelo id

        usuario = Usuario.query.get(user_id)
        if not usuario:
            return {'error': 'Usuário não encontrado', 'status': 'fail'}, 404
        
        # passa os dados_usuario para o método to_dict()
        dados_usuario = usuario.to_dict()
        dados_usuario['status'] = 'success'
        
        # Retorna os dados do usuário em formato JSON
        return dados_usuario, 200
    
    except Exception as e:
        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500
    
def atualizar_usuario(user_id, nome, email, instagram):
    try:
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return {'error': 'Usuário não encontrado'}, 404
        usuario.nome = nome if nome else usuario.nome
        usuario.email = email if email else usuario.email
        usuario.instagram = instagram if instagram else usuario.instagram
        db.session.commit()
        
        # Retorna os dados atualizados passando pelo metodo to_dict()
        dados_usuario = usuario.to_dict()
        dados_usuario['message'] = 'Perfil atualizado com sucesso!'
        dados_usuario['status'] = 'success'
        
        return dados_usuario, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Ocorreu um erro ao atualizar o perfil: {str(e)}', 'status': 'fail'}, 500
    
def salvar_imagem_perfil(user_id, imagem, upload_folder):
    try:
        # Define um nome seguro para o arquivo, incluindo o ID do usuário

        filename = secure_filename(f'{user_id}_{imagem.filename}')
        filepath = os.path.join(upload_folder, filename)

        # Salva a imagem no caminho especificado(upload_folder/ filename)
        imagem.save(filepath)
    
        # Salvar caminho no banco de dados
        usuario = Usuario.query.get(user_id)
        usuario.imagem_perfil = filepath
        db.session.commit()

        return {'message': 'Imagem enviada com sucesso!', 'imagem_url': filepath}, 200
    except Exception as e:
        return {'error': f'Error ao salvar a imagem: {str(e)}'}, 500