from flask_restful import fields
from helpers.database import db

tipoFuncionariosFields = {
    'id': fields.Integer,
    'descricao': fields.String
}

class TipoFuncionario(db.Model):
    __tablename__ = "tipos_funcionarios"  
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, descricao):
        self.descricao = descricao
