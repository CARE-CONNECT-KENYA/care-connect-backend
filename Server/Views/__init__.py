from flask import Blueprint
from flask_restful import Api

api_endpoint = Blueprint

from Server.Views.userview import CountUsers, AddUser,UserLogin,UserResourcesById

api_endpoint= Blueprint('auth',__name__,url_prefix='/care')
api = Api(api_endpoint)


api.add_resource(CountUsers, '/countusers')
api.add_resource(AddUser, '/addusers')
api.add_resource(UserLogin,'/login')
api.add_resource(UserResourcesById, '/users/<int:user_id>')