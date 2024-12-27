from flask_restful import Resource, reqparse, marshal
from models.Relatorio import Relatorio, relatorioFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class RelatoriosResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=True, help="A descrição do relatório é obrigatória.")
        self.parser.add_argument('funcionario_id', type=int, required=True, help="O ID do funcionário é obrigatório.")

    def get(self):
        try:
            relatorios = Relatorio.query.all()
            logger.info("Consulta de relatórios realizada com sucesso!")
            return {'relatorios': marshal(relatorios, relatorioFields)}, 200
        except Exception as e:
            logger.error(f"Erro ao recuperar relatórios: {str(e)}")
            return {"message": f"Erro ao recuperar relatórios: {str(e)}"}, 500

    def post(self):
        args = self.parser.parse_args()
        relatorio = Relatorio(
            descricao=args['descricao'],
            funcionario_id=args['funcionario_id']
        )

        try:
            db.session.add(relatorio)
            db.session.commit()
            logger.info("Relatório cadastrado com sucesso!")
            return marshal(relatorio, relatorioFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar relatório: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar relatório: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500


class RelatorioResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=False, help="A descrição do relatório é obrigatória.")
        self.parser.add_argument('funcionario_id', type=int, required=False, help="O ID do funcionário é obrigatório.")

    def get(self, id):
        try:
            relatorio = Relatorio.query.get(id)
            if not relatorio:
                logger.warning(f"Relatório com ID {id} não encontrado.")
                return {"message": "Relatório não encontrado"}, 404
            logger.info(f"Consulta de relatório ID {id} realizada com sucesso!")
            return {'relatorio': marshal(relatorio, relatorioFields)}, 200
        except Exception as e:
            logger.error(f"Erro ao recuperar relatório: {str(e)}")
            return {"message": f"Erro ao recuperar relatório: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        relatorio = Relatorio.query.get(id)
        if not relatorio:
            logger.warning(f"Relatório com ID {id} não encontrado.")
            return {"message": "Relatório não encontrado"}, 404

        try:
            if args.get("descricao"):
                relatorio.descricao = args["descricao"]
            if args.get("funcionario_id"):
                relatorio.funcionario_id = args["funcionario_id"]

            db.session.commit()
            logger.info(f"Relatório ID {id} atualizado com sucesso!")
            return marshal(relatorio, relatorioFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar relatório ID {id}: {str(e)}")
            return {"message": f"Erro de integridade: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao atualizar relatório ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        relatorio = Relatorio.query.get(id)
        if not relatorio:
            logger.warning(f"Relatório com ID {id} não encontrado.")
            return {"message": "Relatório não encontrado"}, 404

        try:
            db.session.delete(relatorio)
            db.session.commit()
            logger.info(f"Relatório ID {id} excluído com sucesso!")
            return {"message": f"Relatório ID {id} excluído com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir relatório ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro ao excluir relatório: {str(e)}"}, 500
