from flask_restful import Resource, marshal, reqparse
from models.Empresa import Empresa, empresaFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class EmpresasResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=True, help="O nome da empresa é obrigatório.")
        self.parser.add_argument('cnpj', type=str, required=True, help="O CNPJ da empresa é obrigatório.")
        self.parser.add_argument('contato', type=str, required=False, help="O contato da empresa é inválido.")
        self.parser.add_argument('endereco', type=str, required=False, help="O endereço da empresa é inválido.")

    def get(self):
        try: 
            empresas = Empresa.query.all()
            logger.info("Consulta de empresas realizada com sucesso!")
            return {'empresas': marshal(empresas, empresaFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
        
    
    def post(self):
        args = self.parser.parse_args()
        empresa = Empresa(
            nome=args["nome"],
            cnpj=args["cnpj"],
            contato=args.get("contato"),
            endereco=args.get("endereco")  
        )

        try:
            db.session.add(empresa)
            db.session.commit()
            logger.info("Empresa cadastrada com sucesso!")
            return marshal(empresa, empresaFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar empresa: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar empresa: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
