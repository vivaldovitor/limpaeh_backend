from flask_restful import Resource, marshal, reqparse
from models.Ambiente import Ambiente, ambientesFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class AmbientesResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('nome', type=str, required=True, help="O nome do ambiente é obrigatório.")
        self.parse.add_argument('localizacao', type=str, required=False, help="Problema na localização do ambiente.")
        self.parse.add_argument('descricao', type=str, required=False, help="Descrição do ambiente.")

    def get(self):
        ambientes = Ambiente.query.all()
        logger.info("Consulta de ambientes realizada com sucesso!")
        return {'ambientes': marshal(ambientes, ambientesFields)}, 200
