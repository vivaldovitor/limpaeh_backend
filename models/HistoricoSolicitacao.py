from flask_restful import fields
from helpers.database import db
from datetime import datetime, timezone

historicoSolicitacaoFields = {
    'id': fields.Integer,
    'solicitacao_id': fields.Integer,
    'funcionario_origem_id': fields.Integer,
    'funcionario_destino_id': fields.Integer,
    'data_movimentacao': fields.DateTime,
    'descricao_movimentacao': fields.String
}

class HistoricoSolicitacao(db.Model):
    __tablename__ = "historico_solicitacoes"

    id = db.Column(db.Integer, primary_key=True)
    solicitacao_id = db.Column(db.Integer, db.ForeignKey('solicitacoes.id'), nullable=False)
    funcionario_origem_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    funcionario_destino_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=True)
    data_movimentacao = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    descricao_movimentacao = db.Column(db.Text, nullable=True)

    solicitacao = db.relationship('Solicitacao', backref='historico')
    funcionario_origem = db.relationship('Funcionario', foreign_keys=[funcionario_origem_id])
    funcionario_destino = db.relationship('Funcionario', foreign_keys=[funcionario_destino_id])

    def __init__(self, solicitacao_id, funcionario_origem_id, funcionario_destino_id=None, descricao_movimentacao=None):
        self.solicitacao_id = solicitacao_id
        self.funcionario_origem_id = funcionario_origem_id
        self.funcionario_destino_id = funcionario_destino_id
        self.descricao_movimentacao = descricao_movimentacao
