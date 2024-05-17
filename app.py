import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from  flask_cors import CORS
from flask_jwt_extended import JWTManager



app = Flask(__name__)
CORS(app)
db = SQLAlchemy()
jwt = JWTManager()

def initialize_models():
    from Server.Models.users import Users
    from Server.Models.providers import Providers

def initalize_views():
    from Server.Views import api_endpoint
    app.register_blueprint(api_endpoint)

def create_app(config_name):
    app.config.from_object(config_name)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #jwt configurations
    app.config['JWT_SECRET_KEY'] = 'careconnect@dev-inshi'
    app.config['PROPAGATE_EXCEPTIONS'] = True


    # when using mysql
    ###  app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://erick:Erick%40123@localhost/your_db_name' 

    #initializing the db with app
    db.init_app(app)
    # Initialize Flask-Migrate
    migrate = Migrate(app,db)
    jwt.init_app(app)

    #create database schemas
    with app.app_context():
        initialize_models()

    initalize_views()

    return app