from flask_restful import fields
from helpers.database import db

atividadesLimpezaFields = {
    'id': fields.Integer,
    'data_horario_inicio': fields.DateTime,
    'data_horario_fim': fields.DateTime,
    'status': fields.String,
    'ambiente_id': fields.Integer,
    'usuario_id': fields.Integer
}

class AtividadeLimpeza(db.Model):
    __tablename__ = 'atividades_limpeza' 

    id = db.Column(db.Integer, primary_key=True)
    data_horario_inicio = db.Column(db.DateTime, nullable=False)
    data_horario_fim = db.Column(db.DateTime, nullable=True)

    ambiente_id = db.Column(db.Integer, db.ForeignKey('ambientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, data_horario_inicio, ambiente_id, usuario_id, data_horario_fim=None):
        self.data_horario_inicio = data_horario_inicio
        self.data_horario_fim = data_horario_fim
        self.ambiente_id = ambiente_id
        self.usuario_id = usuario_id
