from helpers.database import db
from flask_restful import fields

funcionarioContratoFields = {
    'usuario_id': fields.Integer,
    'contrato_id': fields.Integer
}

class FuncionarioContrato(db.Model):
    __tablename__ = 'funcionarios_contrato'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), primary_key=True)

    usuario = db.relationship('Usuario', lazy=True)
    contrato = db.relationship('Contrato', lazy=True)
