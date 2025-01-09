from flask_restful import Resource, marshal, reqparse
from models.Funcionario import Funcionario, funcionarioFields
from helpers.database import db
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class FuncionariosResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=True, help="O nome do funcionário é obrigatório.")
        self.parser.add_argument('email', type=str, required=True, help="O email do funcionário é obrigatório.")
        self.parser.add_argument('senha', type=str, required=True, help="A senha do funcionário é obrigatória.")
        self.parser.add_argument('tipo_id', type=int, required=True, help="O tipo de funcionário é obrigatório.")
        self.parser.add_argument('empresa_id', type=int, required=False, help="O ID da empresa é opcional.")

    def get(self):
        try:
            funcionarios = Funcionario.query.all()
            logger.info("Consulta de funcionários realizada com sucesso!")
            return {'funcionarios': marshal(funcionarios, funcionarioFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
        
    def post(self):
        args = self.parser.parse_args()
        funcionario = Funcionario(
            nome=args["nome"],
            email=args["email"],
            senha=args["senha"],
            tipo_id=args["tipo_id"],
            empresa_id=args["empresa_id"]
        )

        try:
            db.session.add(funcionario)
            db.session.commit()
            logger.info("Funcionário cadastrado com sucesso!")
            return marshal(funcionario, funcionarioFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar funcionário: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar funcionário: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500


class FuncionarioResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=False, help="O nome do funcionário é obrigatório.")
        self.parser.add_argument('email', type=str, required=False, help="O email do funcionário é obrigatório.")
        self.parser.add_argument('senha', type=str, required=False, help="A senha do funcionário é obrigatória.")
        self.parser.add_argument('tipo_id', type=int, required=False, help="O tipo de funcionário é obrigatório.")
        self.parser.add_argument('empresa_id', type=int, required=False, help="O ID da empresa é opcional.")
   
    def get(self, id):
        try:
            funcionario = Funcionario.query.get(id)
            if funcionario is None:
                logger.warning(f"Funcionário com ID {id} não encontrado.")
                return {"message": "Funcionário não encontrado"}, 404
            
            logger.info(f"Funcionário com ID {id} encontrado com sucesso!")
            return marshal(funcionario, funcionarioFields), 200
        except Exception as e:
            logger.error(f"Ocorreu um erro ao buscar o funcionário com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        funcionario = Funcionario.query.get(id)
        
        if funcionario is None:
            logger.warning(f"Funcionário com ID {id} não encontrado para atualização.")
            return {"message": "Funcionário não encontrado"}, 404
        
        try:
            if args.get("nome"):
                funcionario.nome = args["nome"]
            if args.get("email"):    
                funcionario.email = args["email"]
            if args.get("senha"):   
                funcionario.senha = generate_password_hash(args["senha"])
            if args.get("tipo_id"):
                funcionario.tipo_id = args["tipo_id"]
            if args.get("empresa_id"):
                funcionario.empresa_id = args["empresa_id"]

            db.session.commit()
            logger.info(f"Funcionário com ID {id} atualizado com sucesso!")
            return marshal(funcionario, funcionarioFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar funcionário com ID {id}: {str(e)}")
            return {"message": f"Erro de integridade ao atualizar funcionário: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao atualizar o funcionário com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        funcionario = Funcionario.query.get(id)
        
        if funcionario is None:
            logger.warning(f"Funcionário com ID {id} não encontrado para exclusão.")
            return {"message": "Funcionário não encontrado"}, 404

        try:
            db.session.delete(funcionario)
            db.session.commit()
            logger.info(f"Funcionário com ID {id} excluído com sucesso!")
            return {"message": "Funcionário excluído com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao excluir o funcionário com ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
