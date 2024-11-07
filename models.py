from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipe(db.Model):  # db.Model para o ORM mapear a classe à tabela
    __tablename__ = 'equipes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    # Relacionamento com Ranking e Pontuacao
    rankings = db.relationship('Ranking', backref='equipe', lazy=True)
    pontuacoes = db.relationship('Pontuacao', backref='equipe', lazy=True)
    usuarios = db.relationship('Usuario', backref='equipe', lazy=True)

class Ranking(db.Model):
    __tablename__ = 'rankings'
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    tipo_ranking = db.Column(db.String, nullable=False) 
    pontuacao_total = db.Column(db.Integer, nullable=False)

class Pontuacao(db.Model):
    __tablename__ = 'pontuacoes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)

class Cargo(db.Model):
    __tablename__ = 'cargos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    
    # Relacionamento com um Usuário
    usuarios = db.relationship('Usuario', backref='cargo', lazy=True)
    permissoes = db.relationship('CargoPermissao', back_populates='cargo', lazy=True)

class Permissao(db.Model):
    __tablename__ = 'permissoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    # Relacionamento para vincular Cargos a Permissões
    cargos = db.relationship('CargoPermissao', back_populates='permissao', lazy=True)

class CargoPermissao(db.Model):
    __tablename__ = 'cargo_permissao'
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    permissao_id = db.Column(db.Integer, db.ForeignKey('permissoes.id'), nullable=False)

    # Relacionamento com as tabelas Cargos e Permissões
    cargo = db.relationship('Cargo', back_populates='permissoes')
    permissao = db.relationship('Permissao', back_populates='cargos')


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

    # Relacionamento com Cargo e Equipe
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    equipe_id  = db.Column(db.Integer, db.ForeignKey('equipes.id'),nullable=False)

    instagram = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'