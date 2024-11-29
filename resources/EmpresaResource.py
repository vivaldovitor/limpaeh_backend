from flask_restful import Resource, marshal, reqparse
from models.Empresa import Empresa, empresasFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class EmpresasResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('nome', type=str, required=True, help="O nome da empresa é obrigatório.")
        self.parse.add_argument('cnpj', type=str, required=True, help="O CNPJ da empresa é obrigatório.")
        self.parse.add_argument('contato', type=str, required=False, help="O contato da empresa é inválido.")
        self.parse.add_argument('endereco', type=str, required=False, help="O endereço da empresa é inválido.")

    def get(self):
        empresas = Empresa.query.all()
        logger.info("Consulta de empresas realizada com sucesso!")
        return {'empresas': marshal(empresas, empresasFields)}, 200
