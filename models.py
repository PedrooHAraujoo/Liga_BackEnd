from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipe(db.Model):
    __tablename__ = 'equipes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    # Relacionamento com Ranking, Pontuacao e Usuario
    rankings = db.relationship('Ranking', back_populates='equipe', lazy=True)
    pontuacoes = db.relationship('Pontuacao', back_populates='equipe', lazy=True)
    usuarios = db.relationship('Usuario', back_populates='equipe', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo
        }

class Ranking(db.Model):
    __tablename__ = 'rankings'
    id = db.Column(db.Integer, primary_key=True)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    tipo_ranking = db.Column(db.String, nullable=False)
    pontuacao_total = db.Column(db.Integer, nullable=False)

    equipe = db.relationship('Equipe', back_populates='rankings')

    def to_dict(self):
        return {
            "id": self.id,
            "equipe_id": self.equipe_id,
            "tipo_ranking": self.tipo_ranking,
            "pontuacao_total": self.pontuacao_total,
            "equipe": self.equipe.to_dict() if self.equipe else None
        }

class Pontuacao(db.Model):
    __tablename__ = 'pontuacoes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)

    equipe = db.relationship('Equipe', back_populates='pontuacoes')

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "valor": self.valor,
            "equipe_id": self.equipe_id,
            "data": self.data.isoformat(),
            "equipe": self.equipe.to_dict() if self.equipe else None
        }

class Cargo(db.Model):
    __tablename__ = 'cargos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    usuarios = db.relationship('Usuario', backref='cargo', lazy=True)
    permissoes = db.relationship('CargoPermissao', back_populates='cargo', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
        }

class Permissao(db.Model):
    __tablename__ = 'permissoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    cargos = db.relationship('CargoPermissao', back_populates='permissao', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }

class CargoPermissao(db.Model):
    __tablename__ = 'cargo_permissao'
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    permissao_id = db.Column(db.Integer, db.ForeignKey('permissoes.id'), nullable=False)

    cargo = db.relationship('Cargo', back_populates='permissoes')
    permissao = db.relationship('Permissao', back_populates='cargos')

    def to_dict(self):
        return {
            "id": self.id,
            "cargo_id": self.cargo_id,
            "permissao_id": self.permissao_id,
            "cargo": self.cargo.to_dict() if self.cargo else None,
            "permissao": self.permissao.to_dict() if self.permissao else None
        }

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='pendente', nullable=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=False)
    instagram = db.Column(db.String, nullable=False)

    equipe = db.relationship('Equipe', back_populates='usuarios')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "status": self.status,
            "cargo": self.cargo.to_dict() if self.cargo else None,
            "equipe": self.equipe.to_dict() if self.equipe else None,
            "instagram": self.instagram
        }
