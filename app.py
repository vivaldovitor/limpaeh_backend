from flask import Flask
from helpers.api import api
from helpers.database import db, migrate
from helpers.cors import cors
from flask_jwt_extended import JWTManager
from config import Config
from models.TipoUsuario import TipoUsuario
from helpers.logging import get_logger

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)
api.init_app(app)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY  
jwt = JWTManager(app)

def inserir_tipos_usuarios():
    tipos_iniciais = ["admin", "supervisor", "funcionário"]
    
    for descricao in tipos_iniciais:
        if not TipoUsuario.query.filter_by(descricao=descricao).first():
            novo_tipo = TipoUsuario(descricao=descricao)
            db.session.add(novo_tipo)
    
    db.session.commit()
    get_logger(__name__).info("Inserção de tipos de usuários concluído.")

with app.app_context():
    db.create_all()  
    inserir_tipos_usuarios()


if __name__ == '__main__':
    app.run(debug=True)
