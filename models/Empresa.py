from flask_restful import fields
from helpers.database import db

empresasFields = {
    'id': fields.Integer,
    'nome': fields.String,
    'cnpj': fields.String,
    'contato': fields.String,
    'endereco': fields.String
}

class Empresa(db.Model):
    __tablename__ = 'empresas'  

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    contato = db.Column(db.String(255), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)

    usuarios = db.relationship('Usuario', backref='empresa', lazy=True)

    def __init__(self, nome, cnpj, contato=None, endereco=None):
        self.nome = nome
        self.cnpj = cnpj
        self.contato = contato
        self.endereco = endereco
