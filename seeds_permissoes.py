from models import db, Cargo, Permissao, CargoPermissao
from app import create_app

app = create_app() # Cria a aplicação Flask

def criar_permissoes():
    permissoes = [
        'gerenciar_usuarios', 'visualizar_logs', 'acessar_tudo', 
        'aprovar_usuarios', 'criar_cargo', 'criar_permissao', 
        'editar_cargo', 'editar_permissao', 'deletar_cargo', 
        'deletar_permissao', 'criar_equipe', 'editar_equipe', 
        'deletar_equipe', 'criar_ranking', 'editar_ranking', 
        'deletar_ranking', 'criar_pontuacao', 'editar_pontuacao', 
        'deletar_pontuacao', 'visualizar_equipes', 'visualizar_rankings', 
        'visualizar_historico', 'listar_rankings', 'listar_equipes', 
        'listar_pontuacoes', 'visualizar_pontuacoes', 'listar_usuarios', 
        'visualizar_usuarios'
    ]

    for nome_permissao in permissoes:
        permissao = Permissao(nome=nome_permissao, descricao=nome_permissao.replace('_', ' ').capitalize())
        db.session.add(permissao)
    
    db.session.commit()

def associar_permissoes():
    permissoes_por_cargo = {
        'Admin': [
            'gerenciar_usuarios', 'visualizar_logs', 'acessar_tudo', 
            'aprovar_usuarios', 'criar_cargo', 'criar_permissao', 
            'editar_cargo', 'editar_permissao', 'deletar_cargo', 
            'deletar_permissao', 'criar_equipe', 'editar_equipe', 
            'deletar_equipe', 'criar_ranking', 'editar_ranking', 
            'deletar_ranking', 'criar_pontuacao', 'editar_pontuacao', 
            'deletar_pontuacao', 'visualizar_equipes'
        ],
        'Gerente': [
            'visualizar_rankings', 'visualizar_historico', 
            'visualizar_equipes', 'listar_rankings', 
            'listar_equipes', 'listar_pontuacoes'
        ],
        'Corretor': [
            'visualizar_rankings', 'visualizar_pontuacoes', 
            'listar_rankings', 'listar_pontuacoes'
        ],
        'Assistente de Locação': [
            'visualizar_rankings', 'visualizar_pontuacoes', 
            'listar_pontuacoes', 'listar_equipes'
        ],
        'Suporte': [
            'visualizar_usuarios', 'listar_usuarios'
        ]
    }

    for cargo_nome, permissoes in permissoes_por_cargo.items():
        cargo = Cargo.query.filter_by(nome=cargo_nome).first()
        if not cargo:
            print(f'Cargo {cargo_nome} não encontrado, certifique-se de que o cargo já foi criado.')
            continue

        for nome_permissao in permissoes:
            permissao = Permissao.query.filter_by(nome=nome_permissao).first()
            if permissao:
                cargo_permissao = CargoPermissao(cargo_id=cargo.id, permissao_id=permissao.id)
                db.session.add(cargo_permissao)
    db.session.commit()

if __name__ == '__main__':

    with app.app_context():# Execute as funções para criar permissões e associá-las aos cargos
        criar_permissoes()
        associar_permissoes()
        print('Permissões criadas e assosciadas aos cargos com sucesso!')
