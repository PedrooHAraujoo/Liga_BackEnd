import sqlite3

def conectar_banco():
    conn = sqlite3.connect('pwa.db')
    return conn

def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   tipo TEXT NOT NULL
    );
''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS rankings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   equipe_id INTEGER NOT NULL,
                   tipo_ranking TEXT NOT NULL,
                   pontuacao_total INTEGER NOT NULL,
                   FOREIGN KEY (equipe_id) REFERENCES equipes(id)
    );
''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS pontuacoes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   tipo TEXT NOT NULL,
                   valor INTEGER NOT NULL,
                   equipe_id INTEGER NOT NULL,
                   data DATE NOT NULL,
                   FOREIGN KEY (equipe_id) REFERENCES equipes(id)
    );
''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,    
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                cargo TEXT NOT NULL,
                equipe TEXT NOT NULL, 
                instagram TEXT NOT NULL
    );
''')
    
    conn.commit()
    conn.close()
criar_tabelas()