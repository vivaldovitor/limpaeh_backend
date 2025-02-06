from flask_restful import Resource, marshal, reqparse
from models.Solicitacao import Solicitacao, solicitacaoFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class SolicitacoesResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=True, help="A descrição é obrigatória.")
        self.parser.add_argument('admin_id', type=int, required=True, help="O ID do administrador é obrigatório.")
        self.parser.add_argument('supervisor_id', type=int, required=True, help="O ID do supervisor é opcional.")

    def get(self):
        try:
            solicitacoes = Solicitacao.query.all()
            logger.info("Consulta de solicitações realizada com sucesso!")
            return {'solicitacoes': marshal(solicitacoes, solicitacaoFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def post(self):
        args = self.parser.parse_args()
        solicitacao = Solicitacao(
            descricao=args["descricao"],
            admin_id=args["admin_id"],
            supervisor_id=args["supervisor_id"]
        )

        try:
            db.session.add(solicitacao)
            db.session.commit()
            logger.info("Solicitação cadastrada com sucesso!")
            return marshal(solicitacao, solicitacaoFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar solicitação: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar solicitação: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

class SolicitacaoResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=False)
        self.parser.add_argument('admin_id', type=int, required=False)
        self.parser.add_argument('supervisor_id', type=int, required=False)
        self.parser.add_argument('status', type=str, required=False)

    def get(self, id):
        try:
            solicitacao = Solicitacao.query.get(id)
            if solicitacao is None:
                logger.warning(f"Solicitação com ID {id} não encontrada.")
                return {"message": "Solicitação não encontrada"}, 404

            logger.info(f"Solicitação com ID {id} encontrada com sucesso!")
            return marshal(solicitacao, solicitacaoFields), 200
        except Exception as e:
            logger.error(f"Ocorreu um erro ao buscar a solicitação com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        solicitacao = Solicitacao.query.get(id)

        if solicitacao is None:
            logger.warning(f"Solicitação com ID {id} não encontrada para atualização.")
            return {"message": "Solicitação não encontrada"}, 404

        try:
            if args.get("descricao"):
                solicitacao.descricao = args["descricao"]
            if args.get("admin_id"):
                solicitacao.admin_id = args["admin_id"]
            if args.get("supervisor_id"):
                solicitacao.supervisor_id = args["supervisor_id"]
            if args.get("status"):
                solicitacao.status = args["status"]

            db.session.commit()
            logger.info(f"Solicitação com ID {id} atualizada com sucesso!")
            return marshal(solicitacao, solicitacaoFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar solicitação com ID {id}: {str(e)}")
            return {"message": f"Erro de integridade ao atualizar solicitação: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao atualizar a solicitação com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        solicitacao = Solicitacao.query.get(id)

        if solicitacao is None:
            logger.warning(f"Solicitação com ID {id} não encontrada para exclusão.")
            return {"message": "Solicitação não encontrada"}, 404

        try:
            db.session.delete(solicitacao)
            db.session.commit()
            logger.info(f"Solicitação com ID {id} excluída com sucesso!")
            return {"message": "Solicitação excluída com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao excluir a solicitação com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
