from flask import Flask, request, jsonify
from user import adicionar_usuario

app = Flask(__name__)

@app.route('/cadastrar', methods=['POST'])
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


    resultado, status_code = adicionar_usuario(nome, email, senha, cargo, equipe, instagram)

    
    return jsonify(resultado), status_code

if __name__ == '__main__':
    app.run(debug=True)
