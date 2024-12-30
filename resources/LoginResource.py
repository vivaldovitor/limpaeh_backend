from flask_restful import Resource, reqparse
from models.Funcionario import Funcionario
from helpers.logging import get_logger
from helpers.database import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

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
            # Busca o usuário pelo email
            funcionario = Funcionario.query.filter_by(email=email).first()
            if not funcionario:
                logger.warning(f"Tentativa de login falhou: usuário com email {email} não encontrado.")
                return {"message": "Credenciais inválidas."}, 401

            # Verifica a senha
            if not check_password_hash(funcionario.senha, senha):
                logger.warning(f"Tentativa de login falhou: senha incorreta para o funcionário {email}.")
                return {"message": "Credenciais inválidas."}, 401

            # Gera o token JWT
            access_token = create_access_token(identity={"id": funcionario.id, "email": funcionario.email})

            logger.info(f"Login bem-sucedido para o funcionário {email}.")
            return {
                "message": "Login realizado com sucesso.",
                "token": access_token,
                "usuario_id": funcionario.id
            }, 200

        except Exception as e:
            logger.error(f"Erro ao tentar realizar login: {str(e)}")
            return {"message": "Erro interno no servidor."}, 500
