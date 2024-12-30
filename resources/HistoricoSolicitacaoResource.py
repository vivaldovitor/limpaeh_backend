from flask_restful import Resource, marshal
from models.HistoricoSolicitacao import HistoricoSolicitacao, historicoSolicitacaoFields
from helpers.logging import get_logger

logger = get_logger(__name__)

class HistoricoSolicitacoesResource(Resource):
    def get(self):
        try:
            historicos = HistoricoSolicitacao.query.all()
            logger.info("Consulta de histórico de solicitações realizada com sucesso!")
            return {'historico_solicitacoes': marshal(historicos, historicoSolicitacaoFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

class HistoricoSolicitacaoResource(Resource):
    def get(self, id):
        try:
            historico = HistoricoSolicitacao.query.get(id)
            if historico is None:
                logger.warning(f"Histórico de solicitação com ID {id} não encontrado.")
                return {"message": "Histórico de solicitação não encontrado"}, 404

            logger.info(f"Histórico de solicitação com ID {id} encontrado com sucesso!")
            return marshal(historico, historicoSolicitacaoFields), 200
        except Exception as e:
            logger.error(f"Ocorreu um erro ao buscar o histórico de solicitação com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500