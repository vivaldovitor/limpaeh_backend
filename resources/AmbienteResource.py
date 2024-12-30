from flask_restful import Resource, marshal, reqparse
from models.Ambiente import Ambiente, ambienteFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger
from models.Ambiente import Ambiente

logger = get_logger(__name__)

class AmbientesResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=True, help="O nome do ambiente é obrigatório.")
        self.parser.add_argument('descricao', type=str, required=False, help="Descrição do ambiente.")

    def get(self):
        try:
            page = int(self.parser.parse_args().get('page', 1))
            per_page = int(self.parser.parse_args().get('per_page', 10))

            ambientes = Ambiente.query.paginate(page=page, per_page=per_page, error_out=False).items
            logger.info("Consulta de ambientes realizada com sucesso!")
            return {'ambientes': marshal(ambientes, ambienteFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro ao recuperar ambientes: {str(e)}")
            return {"message": "Erro ao acessar os dados."}, 500

    def post(self):
        args = self.parser.parse_args()

        # Validação de nome duplicado
        if Ambiente.query.filter_by(nome=args['nome']).first():
            return {"message": "Ambiente com este nome já existe."}, 400

        ambiente = Ambiente(
            nome=args['nome'],
            descricao=args.get('descricao')
        )

        try:
            db.session.add(ambiente)
            db.session.commit()
            logger.info(f"Ambiente '{ambiente.nome}' cadastrado com sucesso! ID: {ambiente.id}")
            return marshal(ambiente, ambienteFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar ambiente: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar ambiente: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
        
class AmbienteResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=False, help="Nome do ambiente inválido.")
        self.parser.add_argument('descricao', type=str, required=False, help="Descrição inválida.")

    def get(self, id):
        try:
            ambiente = Ambiente.query.get(id)
            if not ambiente:
                return {"message": "Ambiente não encontrado."}, 404

            logger.info(f"Consulta do ambiente '{ambiente.nome}' realizada com sucesso!")
            return marshal(ambiente, ambienteFields), 200
        except Exception as e:
            logger.error(f"Erro ao recuperar o ambiente: {str(e)}")
            return {"message": f"Erro ao recuperar o ambiente: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        ambiente = Ambiente.query.get(id)
        if not ambiente:
            return {"message": "Ambiente não encontrado."}, 404

        try:
            if args.get('nome') and args['nome'].strip():
                if Ambiente.query.filter_by(nome=args['nome']).first():
                    return {"message": "Ambiente com este nome já existe."}, 400
                ambiente.nome = args['nome']

            if args.get('descricao'):
                ambiente.descricao = args['descricao']

            db.session.commit()
            logger.info(f"Ambiente '{ambiente.nome}' atualizado com sucesso!")
            return marshal(ambiente, ambienteFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar ambiente: {str(e)}")
            return {"message": f"Erro de integridade ao atualizar ambiente: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        ambiente = Ambiente.query.get(id)
        if not ambiente:
            return {"message": "Ambiente não encontrado."}, 404

        try:
            db.session.delete(ambiente)
            db.session.commit()
            logger.info(f"Ambiente '{ambiente.nome}' removido com sucesso!")
            return {"message": f"Ambiente '{ambiente.nome}' removido com sucesso."}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao remover ambiente: {str(e)}")
            return {"message": f"Erro ao remover ambiente: {str(e)}"}, 500
