from flask_restful import fields
from helpers.database import db

tipoUsuarioFields = {
    'id': fields.Integer,
    'descricao': fields.String
}

class TipoUsuario(db.Model):
    __tablename__ = "tipos_usuarios"  
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, descricao):
        self.descricao = descricao
