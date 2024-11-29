from flask_restful import fields
from helpers.database import db

ambientesFields = {
    'id': fields.Integer,
    'nome': fields.String,
    'localizacao': fields.String
}

class Ambiente(db.Model):
    __tablename__ = 'ambientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(255), nullable=True)

    limpezas = db.relationship('AtividadeLimpeza', backref='ambientes', lazy=True, cascade="all, delete-orphan")

    def __init__(self, nome, localizacao=None):
        self.nome = nome
        self.localizacao = localizacao
