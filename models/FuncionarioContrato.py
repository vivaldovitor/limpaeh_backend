from helpers.database import db
from flask_restful import fields

funcionarioContratoFields = {
    'funcionario_id': fields.Integer,
    'contrato_id': fields.Integer
}

class FuncionarioContrato(db.Model):
    __tablename__ = 'funcionarios_contrato'

    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contratos.id'), primary_key=True)

    funcionario = db.relationship('Funcionario', lazy=True)
    contrato = db.relationship('Contrato', lazy=True)
