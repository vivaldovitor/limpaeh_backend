from flask_restful import fields
from helpers.database import db

ambienteFields = {
    'id': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String
}

class Ambiente(db.Model):
    __tablename__ = 'ambientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    limpezas = db.relationship('AtividadeLimpeza', backref='ambientes', lazy=True)

    def __init__(self, nome, descricao=None):
        self.nome = nome
        self.descricao = descricao
