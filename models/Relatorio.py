from flask_restful import fields
from helpers.database import db
from datetime import datetime

relatorioFields = {
    'id': fields.Integer,
    'descricao': fields.String,
    'funcionario_id': fields.Integer,
    'data_hora_criacao': fields.DateTime
}

class Relatorio(db.Model):
    __tablename__ = "relatorios"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_hora_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    funcionario = db.relationship("Usuario", backref=db.backref("relatorios", lazy=True))

    def __init__(self, descricao, funcionario_id):
        self.descricao = descricao
        self.funcionario_id = funcionario_id
