from app import create_app  # Importa a função para criar o app
from crud import criar_equipe, criar_cargo

# Cria o app
app = create_app()

# Contexto da aplicação Flask
with app.app_context():
    # Criar Equipes
    criar_equipe('Conecta', 'Lançamentos')
    criar_equipe('Mar Alto', 'Lançamentos')
    criar_equipe('Barristas', 'Lançamentos')
    criar_equipe('Selecta', 'Lançamentos')
    criar_equipe('Tropa de Elite', 'Seminovos')
    criar_equipe('Diamond', 'Locaçao')

    # Criar Cargos
    criar_cargo('Admin', 'Administrador do Sistema')
    criar_cargo('Gerente', 'Gerente de Equipe')
    criar_cargo('Corretor', 'Corretor de Imoveis')
    criar_cargo('Assistente de Locação', 'Assistente de Locação')
    criar_cargo('Suporte', 'Suporte')
