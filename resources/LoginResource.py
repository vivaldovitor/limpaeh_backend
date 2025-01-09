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

        logger.debug(f"Recebido login para o email: {email} e senha {senha}")

        try:
            funcionario = Funcionario.query.filter_by(email=email).first()
            if not funcionario:
                logger.warning(f"Usuário com email {email} não encontrado no banco de dados.")
                return {"message": "Credenciais inválidas."}, 401

            logger.debug(f"Usuário encontrado: {funcionario.email}")

            if not check_password_hash(funcionario.senha, senha):
                logger.info(f"funcionario.senha = {funcionario.senha} e senha {senha}")
                logger.warning(f"Senha incorreta para o email: {email}")
                return {"message": "Credenciais inválidas."}, 401

            logger.debug("Senha validada com sucesso.")

            access_token = create_access_token(identity={
                "id": funcionario.id,
                "email": funcionario.email,
                "tipo_id": funcionario.tipo_id
            })

            logger.info(f"Login bem-sucedido para o email: {email}")
            return {
                "message": "Login realizado com sucesso.",
                "token": access_token,
                "funcionario_id": funcionario.id,
            }, 200

        except Exception as e:
            logger.error(f"Erro no login: {str(e)}", exc_info=True)
            return {"message": "Erro interno no servidor."}, 500