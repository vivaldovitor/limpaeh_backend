from flask_restful import Resource, marshal, reqparse
from models.AtividadeLimpeza import AtividadeLimpeza, atividadeLimpezaFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class AtividadesLimpezaResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data_horario_inicio', type=str, required=True, help="Data e horário de início são obrigatórios.")
        self.parser.add_argument('data_horario_fim', type=str, required=False, help="Data e horário de fim são opcionais.")
        self.parser.add_argument('status', type=str, required=False, help="Status da atividade de limpeza.")
        self.parser.add_argument('ambiente_id', type=int, required=True, help="ID do ambiente é obrigatório.")
        self.parser.add_argument('funcionario_id', type=int, required=True, help="ID do funcionário é obrigatório.")

    def get(self):
        try:
            atividades_limpeza = AtividadeLimpeza.query.all()
            logger.info("Consulta de atividades de limpeza realizada com sucesso!")
            return {'Atividades': marshal(atividades_limpeza, atividadeLimpezaFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def post(self):
        args = self.parser.parse_args()
        atividade_limpeza = AtividadeLimpeza(
            data_horario_inicio=args['data_horario_inicio'],
            data_horario_fim=args.get('data_horario_fim'),
            status=args.get('status', 'PENDENTE'),
            ambiente_id=args['ambiente_id'],
            funcionario_id=args['funcionario_id']
        )

        try:
            db.session.add(atividade_limpeza)
            db.session.commit()
            logger.info("Atividade de limpeza criada com sucesso!")
            return marshal(atividade_limpeza, atividadeLimpezaFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao inserir atividade de limpeza: {str(e)}")
            return {"message": f"Erro de integridade: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar atividade de limpeza: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500


class AtividadeLimpezaResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data_horario_inicio', type=str, required=False, help="Data e horário de início é inválido.")
        self.parser.add_argument('data_horario_fim', type=str, required=False, help="Data e horário de fim é inválido.")
        self.parser.add_argument('status', type=str, required=False, help="Status é inválido.")
        self.parser.add_argument('ambiente_id', type=int, required=False, help="ID do ambiente é inválido.")
        self.parser.add_argument('funcionario_id', type=int, required=False, help="ID do funcionário é inválido.")

    def get(self, id):
        try:
            atividade = AtividadeLimpeza.query.get(id)
            if not atividade:
                logger.info(f"Atividade de limpeza não encontrada")
                return {"message": "Atividade de limpeza não encontrada."}, 404

            logger.info(f"Consulta da atividade de limpeza {id} realizada com sucesso!")
            return marshal(atividade, atividadeLimpezaFields), 200
        except Exception as e:
            logger.error(f"Erro ao recuperar atividade de limpeza: {str(e)}")
            return {"message": f"Erro ao recuperar atividade de limpeza: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        atividade = AtividadeLimpeza.query.get(id)
        if not atividade:
            return {"message": "Atividade de limpeza não encontrada."}, 404

        try:
            if args.get("data_horario_inicio"):
                atividade.data_horario_inicio = args["data_horario_inicio"]
            if args.get("data_horario_fim"):
                atividade.data_horario_fim = args["data_horario_fim"]
            if args.get("status"):
                atividade.status = args["status"]
            if args.get("ambiente_id"):
                atividade.ambiente_id = args["ambiente_id"]
            if args.get("funcionario_id"):
                atividade.usuario_id = args["funcionario_id"]

            db.session.commit()
            logger.info(f"Atividade de limpeza {id} atualizada com sucesso!")
            return marshal(atividade, atividadeLimpezaFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar atividade de limpeza: {str(e)}")
            return {"message": f"Erro de integridade ao atualizar atividade de limpeza: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar atividade de limpeza: {str(e)}")
            return {"message": f"Erro ao atualizar atividade de limpeza: {str(e)}"}, 500

    def delete(self, id):
        atividade = AtividadeLimpeza.query.get(id)
        if not atividade:
            return {"message": "Atividade de limpeza não encontrada."}, 404

        try:
            db.session.delete(atividade)
            db.session.commit()
            logger.info(f"Atividade de limpeza {id} removida com sucesso!")
            return {"message": "Atividade de limpeza removida com sucesso."}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao remover atividade de limpeza: {str(e)}")
            return {"message": f"Erro ao remover atividade de limpeza: {str(e)}"}, 500
