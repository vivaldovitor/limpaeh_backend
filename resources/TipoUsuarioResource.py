from flask_restful import Resource, marshal, reqparse
from models.TipoUsuario import TipoUsuario, tipoUsuarioFields
from helpers.database import db
from sqlalchemy.exc import IntegrityError
from helpers.logging import get_logger

logger = get_logger(__name__)

class TipoUsuariosResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=True, help="A descrição do tipo de usuário é obrigatória.")

    def get(self):
        try:
            tipos_usuarios = TipoUsuario.query.all()
            logger.info("Consulta de tipos de usuários realizada com sucesso!")
            return {'tipos_usuarios': marshal(tipos_usuarios, tipoUsuarioFields)}, 200
        except Exception as e:
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def post(self):
        args = self.parser.parse_args()
        tipo_usuario = TipoUsuario(
            descricao=args["descricao"]
        )

        try:
            db.session.add(tipo_usuario)
            db.session.commit()
            logger.info("TipoUsuario cadastrado com sucesso!")
            return marshal(tipo_usuario, tipoUsuarioFields), 201
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao cadastrar tipo de usuário: {str(e)}")
            return {"message": f"Erro de integridade ao cadastrar tipo de usuário: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500


class TipoUsuarioResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('descricao', type=str, required=False, help="A descrição do tipo de usuário é obrigatória.")

    def get(self, id):
        try:
            tipo_usuario = TipoUsuario.query.get(id)
            if not tipo_usuario:
                logger.warning(f"TipoUsuario com ID {id} não encontrado.")
                return {"message": "TipoUsuario não encontrado"}, 404
            logger.info(f"Consulta de TipoUsuario ID {id} realizada com sucesso!")
            return {'tipo_usuario': marshal(tipo_usuario, tipoUsuarioFields)}, 200
        except Exception as e:
            logger.error(f"Erro ao recuperar tipo de usuário: {str(e)}")
            return {"message": f"Erro ao recuperar tipo de usuário: {str(e)}"}, 500

    def put(self, id):
        args = self.parser.parse_args()
        tipo_usuario = TipoUsuario.query.get(id)
        if not tipo_usuario:
            logger.warning(f"TipoUsuario com ID {id} não encontrado.")
            return {"message": "TipoUsuario não encontrado"}, 404

        try:
            if args.get("descricao"):
                tipo_usuario.descricao = args["descricao"]

            db.session.commit()
            logger.info(f"TipoUsuario ID {id} atualizado com sucesso!")
            return marshal(tipo_usuario, tipoUsuarioFields), 200
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Erro de integridade ao atualizar tipo de usuário ID {id}: {str(e)}")
            return {"message": f"Erro de integridade: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Ocorreu um erro ao atualizar tipo de usuário ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro: {str(e)}"}, 500

    def delete(self, id):
        tipo_usuario = TipoUsuario.query.get(id)
        if not tipo_usuario:
            logger.warning(f"TipoUsuario com ID {id} não encontrado.")
            return {"message": "TipoUsuario não encontrado"}, 404

        try:
            db.session.delete(tipo_usuario)
            db.session.commit()
            logger.info(f"TipoUsuario ID {id} excluído com sucesso!")
            return {"message": f"TipoUsuario ID {id} excluído com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao excluir tipo de usuário ID {id}: {str(e)}")
            return {"message": f"Ocorreu um erro ao excluir tipo de usuário: {str(e)}"}, 500
