from datetime import datetime
from flask_restful import fields
from helpers.database import db

relatorioFields = {
    'id': fields.Integer,
    'descricao': fields.String,
    'atividade_id': fields.Integer,
    'funcionario_id': fields.Integer,
    'horario_inicio': fields.String,
    'horario_fim': fields.String,
    'observacao': fields.String  
}

class Relatorio(db.Model):
    __tablename__ = "relatorios"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades_limpeza.id'), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=True)
    horario_fim = db.Column(db.Time, nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    funcionario = db.relationship("Funcionario", backref=db.backref("relatorios", lazy=True))
    atividade = db.relationship("AtividadeLimpeza", backref=db.backref("relatorios", lazy=True))

    def __init__(self, descricao, funcionario_id, atividade_id, horario_inicio=None, horario_fim=None, observacao=None):
        self.descricao = descricao
        self.funcionario_id = funcionario_id
        self.atividade_id = atividade_id
        self.horario_inicio = datetime.strptime(horario_inicio, "%H:%M:%S").time() if horario_inicio else None
        self.horario_fim = datetime.strptime(horario_fim, "%H:%M:%S").time() if horario_fim else None
        self.observacao = observacao