from flask_restful import Resource, marshal, reqparse
from models.Usuario import Usuario, usuarioFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class UsuariosResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nome', type=str, required=True, help="O nome do usuário é obrigatório.")
        self.parser.add_argument('email', type=str, required=True, help="O email do usuário é obrigatório.")
        self.parser.add_argument('senha', type=str, required=True, help="A senha do usuário é obrigatória.")
        self.parser.add_argument('tipo_id', type=int, required=True, help="O tipo de usuário é obrigatório.")
        self.parser.add_argument('empresa_id', type=int, required=False, help="O ID da empresa é opcional.")

    def get(self):
        try:
            usuarios = Usuario.query.all()
            logger.info("Consulta de usuários realizada com sucesso!")
            return {'usuarios': marshal(usuarios, usuarioFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
        
    def post(self):
        args = self.parser.parse_args()
        usuario = Usuario(
            nome=args["nome"],
            email=args["email"],
            senha=args["senha"],
            tipo_id=args["tipo_id"],
            empresa_id=args["empresa_id"]
        )

        try:
            db.session.add(usuario)
            db.session.commit()
            logger.info("Usuário cadastrado com sucesso!")
            return marshal(usuario, usuarioFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar usuário: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar usuário: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500
