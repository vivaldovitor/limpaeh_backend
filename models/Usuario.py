from flask_restful import fields
from helpers.database import db
from werkzeug.security import generate_password_hash
from .TipoUsuario import tipoUsuarioFields

usuarioFields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'tipo': fields.Nested(tipoUsuarioFields)
}

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_usuarios.id'), nullable=False)
    tipo = db.relationship("TipoUsuario", backref=db.backref("usuarios", lazy=True))

    def __init__(self, nome, email, senha, tipo_id):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.tipo_id = tipo_id