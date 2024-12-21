from flask_restful import Resource, marshal, reqparse
from models.Ambiente import Ambiente, ambienteFields
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
        try:
            ambientes = Ambiente.query.all()
            logger.info("Consulta de ambientes realizada com sucesso!")
            return {'ambientes': marshal(ambientes, ambienteFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro ao recuperar ambientes: {str(e)}")
            return {"message": "Erro ao acessar os dados."}, 500

    def post(self):
        args = self.parse.parse_args()
        ambiente = Ambiente(
            nome=args['nome'],
            localizacao=args.get('localizacao'),  
            descricao=args.get('descricao') 
        )

        try:
            db.session.add(ambiente)
            db.session.commit()
            logger.info(f"Ambiente '{ambiente.nome}' cadastrado com sucesso!")
            return marshal(ambiente, ambienteFields), 201
        except IntegrityError as e:
            logger.error(f"Erro de integridade ao cadastrar ambiente: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar ambiente: {str(e)}"}, 400
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
