from datetime import datetime
from dateutil import parser
from flask_restful import fields
from helpers.database import db
from .StatusLimpeza import StatusLimpeza

atividadeLimpezaFields = {
    'id': fields.Integer,
    'data_horario_inicio': fields.DateTime,
    'data_horario_fim': fields.DateTime,
    'status': fields.String(attribute=lambda x: x.status.value),
    'descricao': fields.String,
    'ambiente_id': fields.Integer,
    'funcionario_id': fields.Integer,
    'solicitacao_id': fields.Integer
}

class AtividadeLimpeza(db.Model):
    __tablename__ = 'atividades_limpeza'

    id = db.Column(db.Integer, primary_key=True)
    data_horario_inicio = db.Column(db.DateTime, nullable=False)
    data_horario_fim = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(StatusLimpeza), nullable=False, default=StatusLimpeza.PENDENTE)
    descricao = db.Column(db.Text, nullable=True)
    
    ambiente_id = db.Column(db.Integer, db.ForeignKey('ambientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'))

    def __init__(self, data_horario_inicio, descricao, ambiente_id, funcionario_id, solicitacao_id=None, data_horario_fim=None, status=StatusLimpeza.PENDENTE):
        if isinstance(data_horario_inicio, str):
            data_horario_inicio = parser.parse(data_horario_inicio)
        
        if data_horario_inicio > datetime.now():
            raise ValueError("A data de início não pode ser no futuro.")
        
        self.data_horario_inicio = data_horario_inicio
        self.data_horario_fim = data_horario_fim
        self.descricao = descricao
        self.ambiente_id = ambiente_id
        self.funcionario_id = funcionario_id
        self.solicitacao_id = solicitacao_id
        self.status = status
