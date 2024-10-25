from flask import Flask, request, jsonify
from user import adicionar_usuario, redefinir_senha

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
@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha_endpoint():
    data = request.json
    email = data.get('email')
    nova_senha = data.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({'error': 'Preencha o email e a nova senha!'}), 400
    
    resposta, status = redefinir_senha(email, nova_senha)
    return jsonify(resposta), status                

if __name__ == '__main__':
    app.run(debug=True)
