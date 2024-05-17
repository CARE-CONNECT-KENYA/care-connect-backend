import re
from flask import request
from flask_restful import Resource,abort,reqparse
from Server.Models.users import Users
from Server.Models.providers import Providers

from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity


#count tester
class CountProviders(Resource):
    def get(self):
        providerCount = Providers.query.count()
        return {"Providers" : providerCount}, 200
    

class ViewALLProviders(Resource):
    def get(self):
        approvedProviders = Providers.query.filter(Providers.status.in_([True])).order_by(Providers.created_at.desc()).all()

        providersList =[{
            "id": provider.providerID,
            "status" : provider.status,
            "reg_date": provider.created_at,
            "user_id": provider.user_id,
            "name": provider.providerName,
            "bio": provider.bio,
            "email": provider.email,
            "number": provider.phoneNumber,
            "workingHours": provider.workingHours,
            "location": provider.Location,
            "profileImage": provider.profileImage,
            "website": provider.website,
            "services": provider.Services,
            
        } for provider in approvedProviders ]

        return {'providerlist': providersList}, 200
