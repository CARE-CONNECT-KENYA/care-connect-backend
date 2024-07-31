import os
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from  flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message



app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'careconnect621@gmail.com'
app.config['MAIL_PASSWORD'] = 'uqbv mjgp vfgk wyww'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'careconnect621@gmail.com'
mail = Mail(app)


CORS(app)
db = SQLAlchemy()
jwt = JWTManager()

def initialize_models():
    from Server.Models.users import Users
    from Server.Models.providers import Providers
    from Server.Models.reviews import Review
    from Server.Models.facilities import Facilities

def initalize_views():
    from Server.Views import api_endpoint
    app.register_blueprint(api_endpoint)

def create_app(config_name):
    app.config.from_object(config_name)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86000

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



