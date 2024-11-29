from flask_restful import Resource, marshal, reqparse
from models.Usuario import Usuario, usuarioFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class UsuariosResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('nome', type=str, required=True, help="O nome do usuário é obrigatório.")
        self.parse.add_argument('email', type=str, required=True, help="O email do usuário é obrigatório.")
        self.parse.add_argument('senha', type=str, required=True, help="A senha do usuário é obrigatória.")
        self.parse.add_argument('tipo_id', type=int, required=True, help="O tipo de usuário é obrigatório.")
        self.parse.add_argument('empresa_id', type=int, required=False, help="O ID da empresa, se aplicável.")

    def get(self):
        usuarios = Usuario.query.all()
        logger.info("Consulta de usuários realizada com sucesso!")
        return {'usuarios': marshal(usuarios, usuarioFields)}, 200
