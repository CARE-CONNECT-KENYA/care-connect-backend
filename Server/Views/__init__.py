from flask import Blueprint
from flask_restful import Api

api_endpoint = Blueprint


api_endpoint= Blueprint('auth',__name__,url_prefix='/care')
api = Api(api_endpoint)