import bcrypt
from models import db, Usuario

def adicionar_usuario(nome, email, senha, cargo, equipe, instagram):
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
       # Verifica se o email já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return {'error': 'O email já foi registrado.', 'status': 'fail'}, 400
       # Se o email não existe cria um novo usuário
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hashed,
            cargo=cargo,
            equipe=equipe,
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
    