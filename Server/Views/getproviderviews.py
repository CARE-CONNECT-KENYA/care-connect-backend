import re
from flask import jsonify
from flask_restful import Resource
from Server.Models.providers import Providers
from Server.Models.users import Users
from Server.Models.UserInfo import AdditionalUserInfo
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

class GetProviders(Resource):
    @jwt_required()
    def get(self):
        # Retrieve the current user's identity
        current_user_id = get_jwt_identity()

        # Retrieve the current user's additional information
        additional_info = AdditionalUserInfo.query.filter_by(user_id=current_user_id).first()

        # Define the query
        query = Providers.query

        if additional_info:
            if additional_info.location:
                query = query.filter_by(location=additional_info.location)
            elif additional_info.conditions:
                # Prioritize providers by conditions matching their services
                conditions = additional_info.conditions
                query = query.filter(
                    or_(*[Providers.services.contains(condition) for condition in conditions])
                )

        # If no providers matched the location or conditions, order by the latest created
        providers = query.order_by(Providers.created_at.desc()).all()

        # Convert the result to a JSON serializable format
        providers_list = [
            {
                'providerID': provider.providerID,
                'providerName': provider.providerName,
                'location': provider.location,
                'services': provider.services,
                'created_at': provider.created_at,
                'email': provider.email,
                'bio': provider.bio,
                'phonenumber': provider.phoneNumber,

            }
            
            for provider in providers
        ]

        return jsonify(providers_list)

        
                





        

    
