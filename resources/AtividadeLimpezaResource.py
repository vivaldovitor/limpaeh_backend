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
        self.parser.add_argument('usuario_id', type=int, required=True, help="ID do usuário é obrigatório.")
        
    def get(self):
        try:
            atividades_limpeza = AtividadeLimpeza.query.all()
            logger.info("Consulta de atividades de limpeza realizada com sucesso!")
            return {'Atividades': marshal(atividades_limpeza, atividadeLimpezaFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
        
    
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
        self.parser.add_argument('usuario_id', type=int, required=True, help="ID do usuário é obrigatório.")
        
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
            usuario_id=args['usuario_id']
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
