from flask_restful import Resource, marshal, reqparse
from models.AtividadesLimpeza import AtividadeLimpeza, atividadesLimpezaFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class AtividadesLimpezaResource(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('data_horario_inicio', type=str, required=True, help="Data e horário de início são obrigatórios.")
        self.parse.add_argument('data_horario_fim', type=str, required=False, help="Data e horário de fim são opcionais.")
        self.parse.add_argument('status', type=str, required=False, help="Status da atividade de limpeza.")
        self.parse.add_argument('ambiente_id', type=int, required=True, help="ID do ambiente é obrigatório.")
        self.parse.add_argument('usuario_id', type=int, required=True, help="ID do usuário é obrigatório.")
        
    def get(self):
        atividades = AtividadeLimpeza.query.all()
        logger.info("Consulta de atividades de limpeza realizada com sucesso!")
        return {'Atividades': marshal(atividades, atividadesLimpezaFields)}, 200
