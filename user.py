import bcrypt
import jwt
import datetime
from models import db, Usuario, Cargo, Equipe, Ranking
from werkzeug.utils import secure_filename
from flask import jsonify
import os

def adicionar_usuario(nome, email, senha, cargo, equipe, instagram):
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return {'error': 'O email já foi registrado.', 'status': 'fail'}, 400

        cargo_existente = Cargo.query.filter_by(nome=cargo).first()
        if not cargo_existente:
            return {'error': f'Cargo inválido: Cargo={cargo}', 'status': 'fail'}, 400
        status_usuario = 'aprovado' if cargo.lower() in ['admin'] else 'pendente'
        # Cria o novo usuário sem equipe inicialmente
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hashed,
            cargo=cargo_existente,
            instagram=instagram,
            status=status_usuario,
            pontuacao_total=0
        )

        # Adiciona o novo usuário à sessão
        db.session.add(novo_usuario)
        db.session.commit()

        print(f"Usuário {novo_usuario.nome} adicionado com ID: {novo_usuario.id}")

        # Associa a equipe, exceto se for Admin ou Suporte
        if cargo.lower() not in ['admin']:
            equipe_existente = Equipe.query.filter_by(nome=equipe).first()
            if not equipe_existente:
                return {'error': f'Equipe inválida: Equipe={equipe}', 'status': 'fail'}, 400
            novo_usuario.equipe = equipe_existente
            novo_usuario.equipe_id = equipe_existente.id
            db.session.commit()  # Atualiza o usuário com a equipe
            print(f"Usuário {novo_usuario.nome} associado à equipe: {novo_usuario.equipe.nome}")

            # Verifica se a equipe foi associada corretamente
            usuario_atualizado = Usuario.query.get(novo_usuario.id)
            if usuario_atualizado.equipe:
                print(f"Equipe do usuário {usuario_atualizado.nome}: {usuario_atualizado.equipe.nome}")
            else:
                print(f"Equipe do usuário {usuario_atualizado.nome} não foi associada corretamente")

        # Associa o ranking ao novo usuário
        if cargo.lower() == 'admin':
            ranking = Ranking.query.filter_by(nome_ranking="Admin").first()
        elif cargo.lower() == 'gerente':
            ranking = Ranking.query.filter_by(nome_ranking="Gerentes").first()
        else:
            ranking = Ranking.query.filter_by(nome_ranking="Nenhum").first()

        if not ranking:
            return {'error': f'Ranking "{ranking.nome_ranking}" não encontrado.', 'status': 'fail'}, 400

        # Atualiza o campo ranking_atual_id e adiciona o ranking à lista de rankings
        novo_usuario.ranking_atual_id = ranking.id
        novo_usuario.ranking_atual.append(ranking)
        db.session.commit()

        # Verifica se o ranking foi associado corretamente
        if novo_usuario.ranking_atual:
            print(f"Ranking do usuário {novo_usuario.nome}: {[r.nome_ranking for r in novo_usuario.ranking_atual]}")
        else:
            print(f"Ranking do usuário {novo_usuario.nome} não foi associado corretamente")

        return {'message': f'Usuário {nome} foi adicionado com sucesso!', 'status': 'success'}, 201

    except Exception as e:
        db.session.rollback()
        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500

def redefinir_senha(email, nova_senha):
    senha_hashed = bcrypt.hashpw(nova_senha.encode('UTF-8'), bcrypt.gensalt())

    try:
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if not usuario_existente:
            return {'error': 'Usuário não encontrado', 'status': 'fail'}, 404
        
        # Atualiza a senha do usuário
        usuario_existente.senha = senha_hashed
        db.session.commit()

        return {'message': 'Senha redefinida com sucesso!', 'status': 'success'}, 200
    
    except Exception as e:
        db.session.rollback()  # Reverte a transação 

        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500

def login_usuario(email, senha):
    try:
        # Consulta o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário foi encontrado
        if not usuario:
            return {'error': 'Usuário não encontrado', 'status': 'fail'}, 404

        # Verifica se a senha fornecida corresponde à senha armazenada
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
            token = gerar_token(usuario.id)
            return {'token': token, 'status': 'success'}, 200
        else:
            return {'error': 'Credenciais inválidas', 'status': 'fail'}, 401
    except Exception as e:
        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500

def gerar_token(user_id):
    payload = {
        'sub': str(user_id),
        'iat': datetime.datetime.utcnow(),  # Registra o horário em que o token foi gerado
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), 'HS256')
    return token

def verificar_token(token):
    try:
        print(f"Token completo: {token}")
        decoded = jwt.decode(
            token, 
            os.getenv('SECRET_KEY'), 
            algorithms=['HS256'],
        )
        
        return int(decoded.get('sub'))  # Retorna o id do usuário
    
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
        
        # Retorna os dados atualizados passando pelo método to_dict()
        dados_usuario = usuario.to_dict()
        dados_usuario['message'] = 'Perfil atualizado com sucesso!'
        dados_usuario['status'] = 'success'
        
        return dados_usuario, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Ocorreu um erro ao atualizar o perfil: {str(e)}', 'status': 'fail'}, 500

def validar_extensao(arquivo):
    # Extensões permitidas
    extensoes_permitidas = ['png', 'jpg', 'jpeg']
    # Extrai a extensão do arquivo
    extensao = arquivo.rsplit('.', 1)[-1].lower()
    # Verifica se a extensão está na lista de permitidas
    return extensao in extensoes_permitidas

def salvar_imagem_perfil(user_id, imagem, upload_folder):
    try:
        # Valida a extensão do arquivo
        if not validar_extensao(imagem.filename):
            return jsonify({
                'status': 'error',
                'message': 'A extensão do arquivo fornecido é inválida',
                'details': 'Apenas arquivos com as extensões .png, .jpg, .jpeg são permitidos'
            }), 400
        
        # Para uso de debug (para ver o valor de upload_folder)
        print(f"UPLOAD_FOLDER: {upload_folder}")

        # Certifica-se de que o diretório de upload existe
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Define um nome seguro para o arquivo, incluindo o ID do usuário
        filename = secure_filename(f'{user_id}_{imagem.filename}')
        filepath = os.path.join(upload_folder, filename)

        # Salva a imagem no caminho especificado (upload_folder/filename)
        imagem.save(filepath)
    
        # Salvar caminho no banco de dados
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return jsonify({
                'status': 'error',
                'message': 'Usuário não encontrado'
            }), 404
        usuario.imagem_perfil = filepath
        db.session.commit()

        return {'message': 'Imagem enviada com sucesso!', 'imagem_url': filepath}, 200
    except Exception as e:
        return {'error': f'Error ao salvar a imagem: {str(e)}'}, 500
    
