import sqlite3
import bcrypt
from database import conectar_banco

def adicionar_usuario(nome, email, senha, cargo, equipe, instagram):
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        # Verifica se o email já existe no banco de dados
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return {'error': 'O email já foi registrado.', 'status': 'fail'}, 400
        
        # Se o email não existe, insere o novo usuário
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, cargo, equipe, instagram)
            VALUES (?, ?, ?, ?, ?, ?);  
        ''', (nome, email, senha_hashed, cargo, equipe, instagram))
        
        conn.commit()  # Confirma a transação
        return {'message': f'Usuário {nome} foi adicionado com sucesso!', 'status': 'success'}, 201
    
    except sqlite3.Error as e:
        return {'error': f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500
    
    finally:
        conn.close()  # Fecha a conexão com o banco de dados
def redefinir_senha(email, nova_senha):
    senha_hashed = bcrypt.hashpw(nova_senha.encode('UTF-8'), bcrypt.gensalt())

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario_existente = cursor.fetchone()

        if not usuario_existente:
            return{'error': 'Usuário não encontrado', "status" : 'fail'}, 404
        cursor.execute('''
                UPDATE usuarios SET senha = ? WHERE email = ?
''',(senha_hashed, email))
        
        conn.commit()
        return{'message' : 'Senha redefinida com sucesso!', 'status': 'sucess'},200
    except sqlite3.Error as e:
        return{'error' : f'Ocorreu um erro no banco de dados: {str(e)}', 'status': 'fail'}, 500
    finally:
        conn.close()    