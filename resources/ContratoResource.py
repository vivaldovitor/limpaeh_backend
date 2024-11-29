from flask_restful import Resource, marshal, reqparse
from models.Contrato import Contrato, contratoFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class ContratosResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('vigencia_inicio', type=str, required=True, help="A data de início da vigência é obrigatória.")
        self.parse.add_argument('vigencia_fim', type=str, required=True, help="A data de término da vigência é obrigatória.")
        self.parse.add_argument('numero_funcionarios', type=int, required=True, help="O número de funcionários é obrigatório.")
        self.parse.add_argument('custo', type=float, required=True, help="O custo é obrigatório.")
        self.parse.add_argument('empresa_id', type=int, required=True, help="O ID da empresa é obrigatório.")

    def get(self):
        contratos = Contrato.query.all()
        logger.info("Consulta de contratos realizada com sucesso!")
        return {'contratos': marshal(contratos, contratoFields)}, 200
