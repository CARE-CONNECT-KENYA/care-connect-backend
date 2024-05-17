import re
from flask_restful import Resource,abort,reqparse
from Server.Models.users import Users
from Server.Models.providers import Providers
from datetime import datetime
from flask import jsonify,request,make_response
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity


#count tester
class CountProviders(Resource):
    def get(self):
        providerCount = Providers.query.count()
        return {"Providers" : providerCount}, 200
    



class ViewALLProviders(Resource):
    def get(self):
        #### turn this to true 
        approvedProviders = Providers.query.filter(Providers.status.in_([False])).order_by(Providers.created_at.desc()).all()

        providersList =[{
            "id": provider.providerID,
            "status" : provider.status,
            "reg_date": provider.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
            "user_id": provider.user_id,
            "name": provider.providerName,
            "bio": provider.bio,
            "email": provider.email,
            "number": provider.phoneNumber,
            "workingHours": provider.workingHours,
            "location": provider.location,
            "profileImage": provider.profileImage,
            "website": provider.website,
            "services": provider.services,
            
        } for provider in approvedProviders ]

        return {'providerlist': providersList}, 200
 

class AddProvider(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.json
            current_user_id = get_jwt_identity() # Make sure user is logged in

            print(f"Current user: {current_user_id}")

            existing_user = Providers.query.filter_by(user_id=current_user_id).first()
            if existing_user:
                return {"message": "User already has a registered Provider"}, 400
            
            required_fields = ['bio', 'providerName', 'email', 'phoneNumber', 'workingHours', 'profileImage', 'location', 'providerType', 'services']
            for field in required_fields:
                if field not in data:
                    return {"message": f"Missing required field: {field}"}, 400
                
            # Extract all fields
            bio = data.get('bio')
            providerName = data.get('providerName')
            email = data.get('email')
            phoneNumber = data.get('phoneNumber')
            workingHours = data.get('workingHours')
            profileImage = data.get('profileImage')
            website = data.get('website')
            location = data.get('location')
            providerType = data.get('providerType')
            services = data.get('services')

            # Ensure services is a list
            if not isinstance(services, list):
                services = [services]

            # Check for provider with similar name, email, and phone number
            existing_name = Providers.query.filter_by(providerName=providerName).first()
            if existing_name:
                return {"message": f"A provider is already registered with the name: {providerName}"}, 400
            
            existing_email = Providers.query.filter_by(email=email).first()
            if existing_email:
                return {"message": f"The email {email} is already associated with a registered provider"}, 400
            
            existing_phoneNumber = Providers.query.filter_by(phoneNumber=phoneNumber).first()
            if existing_phoneNumber:
                return {"message": f"A provider is already registered with the phone number: {phoneNumber}"}, 400
            
            new_provider = Providers(
                bio=bio,
                providerName=providerName,
                phoneNumber=phoneNumber,
                email=email,
                workingHours=workingHours,
                profileImage=profileImage,
                website=website,
                location=location,
                providerType=providerType,
                services=services,
                user_id=current_user_id
            )

            db.session.add(new_provider)
            db.session.commit()
            return {"message": f"{providerName} registered successfully."}, 201
            

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return make_response(jsonify({"Error": f"Error while registering provider: {str(e)}"}), 500)
