import bcrypt
from database import conectar_banco

def adicionar_usuario(nome, email, senha, cargo, equipe, instagram):
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, cargo, equipe, instagram)
            VALUES (?, ?, ?, ?, ?, ?);  
        ''', (nome, email, senha, cargo, equipe, instagram))
        
        conn.commit()
        print(f'Usuário {nome} foi adicionado com sucesso!')
    except sqlite3.IntegrityError:

        print('Erro: O email já foi registrado.')
    finally:
        conn.close()
