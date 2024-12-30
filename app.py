from flask import Flask
from helpers.api import api
from helpers.database import db, migrate
from helpers.cors import cors
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)
api.init_app(app)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY  
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
