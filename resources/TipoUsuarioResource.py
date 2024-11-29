from flask_restful import Resource, marshal, reqparse
from models.TipoUsuario import TipoUsuario, tipoUsuarioFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class TipoUsuarioResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('descricao', type=str, required=True, help="A descrição do tipo de usuário é obrigatória.")

    def get(self):
        tipos_usuarios = TipoUsuario.query.all()
        logger.info("Consulta de tipos de usuários realizada com sucesso!")
        return {'tipos_usuarios': marshal(tipos_usuarios, tipoUsuarioFields)}, 200
