import datetime
from flask_restful import fields
from helpers.database import db
from .StatusLimpeza import StatusLimpeza

atividadeLimpezaFields = {
    'id': fields.Integer,
    'data_horario_inicio': fields.DateTime,
    'data_horario_fim': fields.DateTime,
    'status': fields.String(attribute=lambda x: x.status.value),
    'ambiente_id': fields.Integer,
    'usuario_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

class AtividadeLimpeza(db.Model):
    __tablename__ = 'atividades_limpeza'

    id = db.Column(db.Integer, primary_key=True)
    data_horario_inicio = db.Column(db.DateTime, nullable=False)
    data_horario_fim = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(StatusLimpeza), nullable=False, default=StatusLimpeza.PENDENTE)

    ambiente_id = db.Column(db.Integer, db.ForeignKey('ambientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, data_horario_inicio, ambiente_id, usuario_id, data_horario_fim=None, status=StatusLimpeza.PENDENTE):
        if data_horario_inicio > datetime.now():
            raise ValueError("A data de início não pode ser no futuro.")
        self.data_horario_inicio = data_horario_inicio
        self.data_horario_fim = data_horario_fim
        self.ambiente_id = ambiente_id
        self.usuario_id = usuario_id
        self.status = status
