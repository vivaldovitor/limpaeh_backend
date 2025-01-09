from flask_restful import fields
from helpers.database import db
from datetime import datetime, timezone
from .StatusSolicitacao import StatusSolicitacao

solicitacaoFields = {
    'id': fields.Integer,
    'descricao': fields.String,
    'status': fields.String(attribute=lambda x: x.status.value),
    'setor_admin_id': fields.Integer,
    'supervisor_id': fields.Integer,
    'data_criacao': fields.DateTime,
    'data_finalizacao': fields.DateTime
}

class Solicitacao(db.Model):
    __tablename__ = "solicitacoes"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(StatusSolicitacao), nullable=False, default=StatusSolicitacao.PENDENTE)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    data_finalizacao = db.Column(db.DateTime, nullable=True)

    setor_admin_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)  
    supervisor_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    
    atividades = db.relationship('AtividadeLimpeza', backref='solicitacao', lazy=True)
    
    setor_admin = db.relationship('Funcionario', foreign_keys=[setor_admin_id], backref='solicitacoes_criadas')
    supervisor = db.relationship('Funcionario', foreign_keys=[supervisor_id], backref='solicitacoes_supervisionadas')

    def __init__(self, descricao, setor_admin_id, supervisor_id):
        self.descricao = descricao
        self.setor_admin_id = setor_admin_id
        self.supervisor_id = supervisor_id
