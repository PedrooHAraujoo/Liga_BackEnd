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
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    cargo = db.Column(db.String, nullable=False)
    equipe = db.Column(db.String, nullable=False)
    instagram = db.Column(db.String, nullable=False)