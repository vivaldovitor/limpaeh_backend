from flask_restful import Resource, marshal, reqparse
from models.FuncionarioContrato import FuncionarioContrato, funcionarioContratoFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class FuncionariosContratoResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('usuario_id', type=int, required=True, help='Problema no usuario_id')
        self.parser.add_argument('contrato_id', type=int, required=True, help='Problema no contrato_id')  

    def get(self):
        try:
            funcionarios_contratos = FuncionarioContrato.query.all()
            logger.info('Consulta realizada com sucesso!')
            return {'funcionarios_contratos': marshal(funcionarios_contratos, funcionarioContratoFields)}, 200
        except Exception as e:
            logger.error(f'Erro ao recuperar funcionários de contrato: {str(e)}')
            return {'message': 'Erro ao acessar os dados.'}, 500
        
    
    def post(self):
        args = self.parser.parse_args()
        funcionario_contrato = FuncionarioContrato(
            usuario_id=args["usuario_id"],
            contrato_id=args["contrato_id"]  
        )

        try:
            db.session.add(funcionario_contrato)
            db.session.commit()
            logger.info("FuncionarioContrato cadastrado com sucesso!")
            return marshal(funcionario_contrato, funcionarioContratoFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de Integridade ao cadastrar funcionário contrato: {str(e)}")
            return {"message": f"Erro de Integridade ao cadastrar funcionário contrato: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
