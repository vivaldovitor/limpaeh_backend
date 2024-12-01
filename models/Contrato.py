from flask_restful import fields
from helpers.database import db

contratoFields = {
    'id': fields.Integer,
    'vigencia_inicio': fields.DateTime,
    'vigencia_fim': fields.DateTime,
    'numero_funcionarios': fields.Integer,
    'custo': fields.Float
}

class Contrato(db.Model):
    __tablename__ = 'contratos' 

    id = db.Column(db.Integer, primary_key=True)  
    vigencia_inicio = db.Column(db.DateTime, nullable=False)  
    vigencia_fim = db.Column(db.DateTime, nullable=False)  
    numero_funcionarios = db.Column(db.Integer, nullable=False) 
    custo = db.Column(db.Float, nullable=False)  

    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)  
    empresa = db.relationship('Empresa', backref=db.backref('contratos', lazy=True))

    usuarios = db.relationship('Usuario', secondary='funcionarios_contrato', backref=db.backref('contratos', lazy=True))  

    def __init__(self, vigencia_inicio, vigencia_fim, numero_funcionarios, custo, empresa_id):
        self.vigencia_inicio = vigencia_inicio
        self.vigencia_fim = vigencia_fim
        self.numero_funcionarios = numero_funcionarios
        self.custo = custo
        self.empresa_id = empresa_id
