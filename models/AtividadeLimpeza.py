from flask_restful import fields
from helpers.database import db
from .StatusLimpeza import StatusLimpeza

atividadeLimpezaFields = {
    'id': fields.Integer,
    'status': fields.String(attribute=lambda x: x.status.value),
    'descricao': fields.String,
    'funcionario_id': fields.Integer,
    'ambiente_id': fields.Integer,
}

class AtividadeLimpeza(db.Model):
    __tablename__ = 'atividades_limpeza'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(StatusLimpeza), nullable=False, default=StatusLimpeza.PENDENTE)
    ambiente_id = db.Column(db.Integer, db.ForeignKey('ambientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)

    def __init__(self, descricao, ambiente_id, funcionario_id, status=StatusLimpeza.PENDENTE):
        self.descricao = descricao
        self.ambiente_id = ambiente_id
        self.funcionario_id = funcionario_id
        self.status = status