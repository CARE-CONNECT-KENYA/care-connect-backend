from flask_restful import Resource
from Server.Models.users import Users
from flask import jsonify,request,make_response
from datetime import datetime, timedelta
from flask_jwt_extended import get_current_user
import jwt

from functools import wraps
import json


from app import db,jwt 



class CountUsers(Resource):
    def get(self):
        users_count = Users.query.count()
        return {"total users": users_count}, 200
    

#  define user roles 
def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user = get_current_user()
            roles = role if isinstance(role, list) else [role]
            if all(not current_user.has_role(r) for r in roles):
                return make_response({"msg": f"Missing any of roles {','.join(roles)}"}, 403)
            return fn(*args, **kwargs)

        return decorator

    return wrapper

@jwt.user_identity_loader
def user_identity_lookup(user):
    if isinstance(user, Users):
        return user.id
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Users.query.filter_by(id=identity).one_or_none()