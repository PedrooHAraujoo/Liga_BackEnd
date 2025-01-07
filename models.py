from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    nome_ranking = db.Column(db.String, nullable=False, default="Nenhum")  # Nome do ranking
    tipo = db.Column(db.String, nullable=True)  # Categoria ou tipo do ranking
    meta_pontuacao = db.Column(db.Integer, nullable=False, default=0)  # Meta para atingir este ranking

    def to_dict(self):
        return {
            "id": self.id,
            "nome_ranking": self.nome_ranking,
            "tipo": self.tipo,
            "meta_pontuacao": self.meta_pontuacao
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
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'), nullable=True) # Vinculação opcional para Admin ou Suporte
    instagram = db.Column(db.String)
    status = db.Column(db.String, default='pendente', nullable=False)
    pontuacao_total = db.Column(db.Integer, default=0, nullable=False)  # Pontuação acumulada do usuário
    ranking_atual_id = db.Column(db.Integer, db.ForeignKey('rankings.id'), nullable=True)  # Ranking atual

    ranking_atual = db.relationship('Ranking')  # Relacionamento com o ranking atual
    pontuacoes = db.relationship('Pontuacao', back_populates='usuario', lazy=True) # Relacionamento com as pontuações
    
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
            "ranking_atual": self.ranking_atual.to_dict() if self.ranking_atual else None
        }