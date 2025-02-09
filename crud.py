from models import db, Equipe, Ranking, Permissao, Pontuacao, Cargo, CargoPermissao, Usuario

# Funções CRUD para Equipe
def criar_equipe(nome, tipo):
    equipe = Equipe(nome=nome, tipo=tipo)
    db.session.add(equipe)
    db.session.commit()

    return equipe

def listar_equipes():
    return Equipe.query.all()

def atualizar_equipe(id, nome=None, tipo=None):
    equipe = Equipe.query.get(id)
    if equipe:
        if nome:
            equipe.nome = nome
        if tipo:
            equipe.tipo = tipo
        db.session.commit()
    return equipe

def deletar_equipe(id):
    equipe = Equipe.query.get(id)
    if equipe:
        db.session.delete(equipe)
        db.session.commit()
        return True
    return False

# Funções Crud para Ranking
def criar_ranking(nome_ranking, tipo, meta_pontuacao):
    ranking = Ranking(nome_ranking=nome_ranking, tipo=tipo ,meta_pontuacao=meta_pontuacao)
    db.session.add(ranking)
    db.session.commit()
    
    return ranking

def listar_ranking():
    return Ranking.query.all()

def atualizar_ranking(id, nome_ranking=None, meta_pontuacao=None):
    ranking = Ranking.query.get(id)
    if ranking:
        if nome_ranking:
            ranking.nome_ranking = nome_ranking
        if meta_pontuacao:
            ranking.meta_pontuacap = meta_pontuacao
        db.session.commit()
    return ranking

def deletar_ranking(id):
    ranking = Ranking.query.get(id)
    if ranking:
        db.session.delete(ranking)
        db.session.commit()
        return True
    return False

# Funções Crud para Pontuação
def criar_pontuacao(tipo, valor, usuario_id, data):
    pontuacao = Pontuacao(tipo=tipo, valor=valor, usuario_id=usuario_id, data=data)
    db.session.add(pontuacao)
    db.session.commit()
    return pontuacao

def listar_pontuacao():
    return Pontuacao.query.all()

def atualizar_pontuacao(id, tipo=None, valor=None, usuario_id=None, data=None):
    pontuacao = Pontuacao.query.get(id)
    if pontuacao:
        if tipo:
            pontuacao.tipo = tipo
        if valor:
            pontuacao.valor = valor
        if usuario_id:
            pontuacao.usuario_id = usuario_id
        if data:
            pontuacao.data = data
        db.session.commit()
    return pontuacao

def deletar_pontuacao(id):
    pontuacao = Pontuacao.query.get(id)
    if pontuacao:
        db.session.delete(pontuacao)
        db.session.commit()
        return True
    return False

# Funções CRUD para Cargo
def criar_cargo(nome, descricao=''):
    cargo = Cargo(nome=nome, descricao=descricao)
    db.session.add(cargo)
    db.session.commit()
    return cargo

def listar_cargos():
    return Cargo.query.all()

def atualizar_cargo(id, nome=None, descricao=None):
    cargo = Cargo.query.get(id)
    if cargo:
        if nome:
            cargo.nome = nome
        if descricao:
            cargo.descricao = descricao
        db.session.commit()
    return cargo

def deletar_cargo(id):
    cargo = Cargo.query.get(id)
    if cargo:
        db.session.delete(cargo)
        db.session.commit()
        return True
    return False

# Funçoes CRUD para Permissao
def criar_permissao(nome, descricao=""):
    permissao = Permissao(nome=nome, descricao=descricao)
    db.session.add(permissao)
    db.session.commit()
    return permissao

def listar_permissoes():
    return Permissao.query.all()

def atualizar_permissao(id, nome=None, descricao=None):
    permissao = Permissao.query.get(id)
    if permissao:
        if nome:
            permissao.nome = nome
        if descricao:
            permissao.descricao = descricao
        db.session.commit()
    return permissao

def deletar_permissao(id):
    permissao = Permissao.query.get(id)
    if permissao:
        db.session.delete(permissao)
        db.session.commit()
        return True
    return False

# Funções para associar e desassociar Permissões a Cargo
def associar_permissoes_cargo(cargo_id, permissao_id):
    if not Cargo.query.get(cargo_id) or not Permissao.query.get(permissao_id):
        return None
    associacao = CargoPermissao(cargo_id=cargo_id, permissao_id=permissao_id)
    db.session.add(associacao)
    db.session.commit()
    return associacao

def desassociar_permissao_cargo(cargo_id, permissao_id):
    associacao = CargoPermissao.query.filter_by(cargo_id=cargo_id, permissao_id=permissao_id).first()
    if associacao:
        db.session.delete(associacao)
        db.session.commit()
        return True
    return False

# Funções CRUD para Usuário (Admin)
def criar_usuario(nome, email, senha, cargo_id, equipe_id, instagram, ranking=None, pontuacao=None):
    usuario = Usuario(nome=nome, email=email, senha=senha, cargo_id=cargo_id, instagram=instagram, ranking=ranking, pontuacao=pontuacao)
    
    # Associa a equipe, exceto se for Admin ou Suporte
    cargo_nome= Cargo.query.get(cargo_id).nome.lower()
    if cargo_nome not in ['admin', 'suporte'] and equipe_id:
        usuario.equipe_id = equipe_id

    db.session.add(usuario)
    db.session.commit()
    return usuario

def listar_usuarios():
    return Usuario.query.all()

def atualizar_usuario(id, nome=None, email=None, senha=None, cargo_id=None, equipe_id=None, instagram=None, ranking=None, pontuacao=None):
    usuario = Usuario.query.get(id)
    if usuario:
        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if senha:
            usuario.senha = senha
        if cargo_id:
            usuario.cargo_id = cargo_id
        if equipe_id:
            cargo_nome = Cargo.query.get(cargo_id).nome.lower()
            if cargo_nome not in ['admin', 'suporte']:
                usuario.equipe_id = equipe_id
        if instagram:
            usuario.instagram = instagram
        if ranking is not None:
            usuario.ranking = ranking
        if pontuacao is not None:
            usuario.pontuacao = pontuacao
        db.session.commit()
    return usuario

def deletar_usuario_crud(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return True
    return False