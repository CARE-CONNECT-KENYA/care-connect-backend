import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Mail configuration from environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True').lower() == 'true'
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
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

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86000))

    # JWT configurations
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Initialize the DB with the app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    # Create database schemas
    with app.app_context():
        initialize_models()

    initalize_views()

    return app
