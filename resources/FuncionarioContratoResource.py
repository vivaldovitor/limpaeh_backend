from flask_restful import Resource, marshal, reqparse
from models.FuncionarioContrato import FuncionarioContrato, funcionario_contrato_fields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class FuncionariosContratoResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('usuario_id', type=int, help='Problema no usuario_id')
        self.parser.add_argument('contrato_id', type=int, help='Problema no contrato_id')

    def get(self):
        try:
            funcionarios_contratos = FuncionarioContrato.query.all()
            logger.info('Consulta realizada com sucesso!')
            
            if not funcionarios_contratos:
                logger.warning('Nenhum registro encontrado para FuncionarioContrato.')
                return {'message': 'Nenhum funcionário de contrato encontrado'}, 404

            return {'funcionarios_contratos': [marshal(fc, funcionario_contrato_fields) for fc in funcionarios_contratos]}

        except Exception as e:
            logger.error(f'Erro ao recuperar funcionários de contrato: {str(e)}')
            return {'message': 'Erro ao acessar os dados.'}, 500
