from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela de associação muitos-para-muitos entre Usuario e Ranking
usuario_ranking_association = db.Table('usuario_ranking_association',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('ranking_id', db.Integer, db.ForeignKey('rankings.id'), primary_key=True)
)

class Equipe(db.Model):
    __tablename__ = 'equipes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo
        }

class Ranking(db.Model):
    __tablename__ = 'rankings'
    id = db.Column(db.Integer, primary_key=True)
    nome_ranking = db.Column(db.String, nullable=False, default="Nenhum")
    tipo = db.Column(db.String, nullable=True)
    meta_pontuacao = db.Column(db.Integer, nullable=False, default=0)

    # Relacionamento muitos-para-muitos com Usuario
    usuarios = db.relationship('Usuario', secondary=usuario_ranking_association, back_populates='ranking_atual')

    def to_dict(self):
        return {
            "id": self.id,
            "nome_ranking": self.nome_ranking,
            "tipo": self.tipo,
            "meta_pontuacao": self.meta_pontuacao,
            "usuarios": [usuario.id for usuario in self.usuarios]
        }

class Pontuacao(db.Model):
    __tablename__ = 'pontuacoes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Vinculação com usuários
    data = db.Column(db.Date, nullable=False)

    usuario = db.relationship('Usuario', back_populates='pontuacoes') # Relacionamento com usuários

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "valor": self.valor,
            "usuario_id": self.usuario_id,
            "data": self.data.isoformat(),
            "usuario": self.usuario.to_dict() if self.usuario else None
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
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargos.id'))
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=True)
    instagram = db.Column(db.String)
    status = db.Column(db.String, default='pendente', nullable=False)
    pontuacao_total = db.Column(db.Integer, default=0, nullable=False)
    ranking_atual_id = db.Column(db.Integer, db.ForeignKey('rankings.id'), nullable=True)

    # Relacionamento muitos-para-muitos com Ranking
    ranking_atual = db.relationship('Ranking', secondary=usuario_ranking_association, back_populates='usuarios', overlaps="ranking_atual,usuarios") 
    equipe = db.relationship('Equipe', backref=db.backref('membros', lazy=True)) # Relacionamento com Equipe
    pontuacoes = db.relationship('Pontuacao', back_populates='usuario', lazy=True) # Relacionamento com Pontuações

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cargo_id": self.cargo_id,
            "equipe_id": self.equipe_id,
            "instagram": self.instagram,
            "status": self.status,
            "pontuacao_total": self.pontuacao_total,
            "ranking_atual": [ranking.to_dict() for ranking in self.ranking_atual] if self.ranking_atual else None, # Lista de rankings
            "equipe": self.equipe.to_dict() if self.equipe else None # Verifica se a equipe é None
        }
