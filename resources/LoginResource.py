from flask_restful import Resource, reqparse
from models.Usuario import Usuario
from helpers.logging import get_logger
from helpers.database import db
from werkzeug.security import check_password_hash

logger = get_logger(__name__)

class LoginResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help="O email é obrigatório.")
        self.parser.add_argument('senha', type=str, required=True, help="A senha é obrigatória.")

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        senha = args['senha']

        try:
            usuario = Usuario.query.filter_by(email=email).first()
            if not usuario:
                logger.warning(f"Tentativa de login falhou: usuário com email {email} não encontrado.")
                return {"message": "Credenciais inválidas."}, 401

            if not check_password_hash(usuario.senha, senha):
                logger.warning(f"Tentativa de login falhou: senha incorreta para o usuário {email}.")
                return {"message": "Credenciais inválidas."}, 401

            logger.info(f"Login bem-sucedido para o usuário {email}.")
            return {"message": "Login realizado com sucesso.", "usuario_id": usuario.id}, 200

        except Exception as e:
            logger.error(f"Erro ao tentar realizar login: {str(e)}")
            return {"message": "Erro interno no servidor."}, 500
