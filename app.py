from flask import Flask, request, render_template, redirect, url_for, jsonify
from user import adicionar_usuario

app = Flask(__name__)

@app.route('/cadastrar', methods = ['POST'])
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
    adicionar_usuario(nome, email, senha, cargo, equipe, instagram)
    return jsonify({'message': f'Usuário {nome} foi adicionado com sucesso"'})
if __name__ == '__main__':
    app.run(debug=True)
