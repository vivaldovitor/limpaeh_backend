from flask_restful import Resource, marshal, reqparse
from models.Contrato import Contrato, contratoFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class ContratosResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('vigencia_inicio', type=str, required=True, help="A data de início da vigência é obrigatória.")
        self.parser.add_argument('vigencia_fim', type=str, required=True, help="A data de término da vigência é obrigatória.")
        self.parser.add_argument('numero_funcionarios', type=int, required=True, help="O número de funcionários é obrigatório.")
        self.parser.add_argument('custo', type=float, required=True, help="O custo é obrigatório.")
        self.parser.add_argument('empresa_id', type=int, required=True, help="O ID da empresa é obrigatório.")

    def get(self):
        try:    
            contratos = Contrato.query.all()
            logger.info("Consulta de contratos realizada com sucesso!")
            return {'contratos': marshal(contratos, contratoFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def post(self):
        args = self.parser.parse_args()
        contrato = Contrato(
            vigencia_inicio=args["vigencia_inicio"],
            vigencia_fim=args["vigencia_fim"],
            numero_funcionarios=args["numero_funcionarios"],
            custo=args["custo"],
            empresa_id=args["empresa_id"]
        )

        try:
            db.session.add(contrato)
            db.session.commit()
            logger.info("Contrato cadastrado com sucesso!")
            return marshal(contrato, contratoFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro de integridade ao cadastrar contrato: {str(e)}")
            return {"message": f"Ocorreu um erro de integridade ao cadastrar contrato: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500


class ContratoResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('vigencia_inicio', type=str, required=False, help="A data de início da vigência é inválida.")
        self.parser.add_argument('vigencia_fim', type=str, required=False, help="A data de término da vigência é inválida.")
        self.parser.add_argument('numero_funcionarios', type=int, required=False, help="O número de funcionários é inválido.")
        self.parser.add_argument('custo', type=float, required=False, help="O custo é inválido.")
        self.parser.add_argument('empresa_id', type=int, required=False, help="O ID da empresa é inválido.")

    def get(self, id):
        try:
            contrato = Contrato.query.get(id)
            if not contrato:
                logger.info(f"Contrato com ID {id} não encontrado.")
                return {"message": "Contrato não encontrado."}, 404

            logger.info(f"Consulta do contrato {id} realizada com sucesso!")
            return marshal(contrato, contratoFields), 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        contrato = Contrato.query.get(id)
        if not contrato:
            return {"message": "Contrato não encontrado."}, 404

        try:
            if args.get("vigencia_inicio"):
                contrato.vigencia_inicio = args["vigencia_inicio"]
            if args.get("vigencia_fim"):
                contrato.vigencia_fim = args["vigencia_fim"]
            if args.get("numero_funcionarios"):
                contrato.numero_funcionarios = args["numero_funcionarios"]
            if args.get("custo"):
                contrato.custo = args["custo"]
            if args.get("empresa_id"):
                contrato.empresa_id = args["empresa_id"]

            db.session.commit()
            logger.info(f"Contrato {id} atualizado com sucesso!")
            return marshal(contrato, contratoFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar contrato: {str(e)}")
            return {"message": f"Erro de integridade ao atualizar contrato: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        contrato = Contrato.query.get(id)
        if not contrato:
            return {"message": "Contrato não encontrado."}, 404

        try:
            db.session.delete(contrato)
            db.session.commit()
            logger.info(f"Contrato {id} removido com sucesso!")
            return {"message": "Contrato removido com sucesso."}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao remover contrato: {str(e)}")
            return {"message": f"Ocorreu um erro ao remover contrato: {str(e)}"}, 500
