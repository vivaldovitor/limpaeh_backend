from flask_restful import fields
from helpers.database import db
from datetime import datetime, timezone
from .StatusSolicitacao import StatusSolicitacao

solicitacaoFields = {
    'id': fields.Integer,
    'descricao': fields.String,
    'status': fields.String(attribute=lambda x: x.status.value),
    'admin_id': fields.Integer,
    'supervisor_id': fields.Integer,
}

class Solicitacao(db.Model):
    __tablename__ = "solicitacoes"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusSolicitacao), nullable=False, default=StatusSolicitacao.ENVIADO)

    admin_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)  
    supervisor_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
        
    admin = db.relationship('Funcionario', foreign_keys=[admin_id], backref='solicitacoes_criadas')
    supervisor = db.relationship('Funcionario', foreign_keys=[supervisor_id], backref='solicitacoes_supervisionadas')

    def __init__(self, descricao, admin_id, supervisor_id):
        self.descricao = descricao
        self.admin_id = admin_id
        self.supervisor_id = supervisor_id
