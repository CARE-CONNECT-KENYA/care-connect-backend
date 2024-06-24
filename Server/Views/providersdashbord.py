from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify,request,make_response
from Server.Models.providers import Providers
from Server.Models.users import Users
from datetime import datetime
from app import db
from functools import wraps

def check_role(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = Users.query.get(current_user_id)
            if user and user.role != required_role:
                 return make_response( jsonify({"error": "Unauthorized access"}), 403 )       
            return fn(*args, **kwargs)
        return decorator
    return wrapper

class SpecificUserProvider(Resource):
    @jwt_required()
    @check_role('admin')
    def get(self):
        current_user_id = get_jwt_identity()
        my_provider = Providers.query.filter_by(user_id=current_user_id).first()

        if my_provider:
            provider_details = {
                'providerID': my_provider.providerID,
                "name": my_provider.providerName,
                'providerName': my_provider.providerName,
                'location': my_provider.location,
                'services': my_provider.services,
                "workingHours": my_provider.workingHours,
                'created_at': my_provider.created_at.strftime('%Y-%m-%d %H:%M:%S'),  
                'email': my_provider.email,
                "profileImage": my_provider.profileImage,
                'bio': my_provider.bio,
                "website": my_provider.website,
                'phonenumber': my_provider.phoneNumber,
                "services": my_provider.services,
            }
            response = make_response(jsonify(provider_details), 200)
        else:
            response = make_response(jsonify({'message': 'Provider not found'}), 404)
        
        return response
        
        

    @jwt_required()
    @check_role('admin')
    def put(self):
        try:
            current_user_id = get_jwt_identity()
            my_provider = Providers.query.filter_by(user_id=current_user_id).first()

            if not my_provider:
                return {"error": "User does not have provider details"}, 404

            data = request.get_json()
            # Update provider details
            my_provider.providerName = data.get('providerName', my_provider.providerName)
            my_provider.location = data.get('location', my_provider.location)
            my_provider.services = data.get('services', my_provider.services)
            my_provider.email = data.get('email', my_provider.email)
            my_provider.bio = data.get('bio', my_provider.bio)
            my_provider.phoneNumber = data.get('phoneNumber', my_provider.phoneNumber)
            my_provider.workingHours = data.get('wokingHours'), my_provider.workingHours
            my_provider.profileImage = data.get('profileImage'), my_provider.profileImage,
            my_provider.website = data.get('website'), my_provider.website

            db.session.commit()

            return {"message": "Provider details updated successfully"}, 200
        
        except Exception as e:
            return {"message": f"Error updating provider details: {str(e)}"}, 500

    @jwt_required()
    @check_role('admin')
    def delete(self):
        try:
            current_user_id = get_jwt_identity()
            my_provider = Providers.query.filter_by(user_id=current_user_id).first()

            if not my_provider:
                return {"error": "User does not have provider details"}, 404

            db.session.delete(my_provider)
            db.session.commit()

            return {"message": "Provider details deleted successfully"}, 200
        
        except Exception as e:
            return {"message": f"Error deleting provider details: {str(e)}"}, 500

# Not tested but should allow users to add a new admin
class GrantAdminAccess(Resource):
    @jwt_required()
    @check_role('admin')
    def post(self):
        try:
            data = request.get_json()
            user_ids = data.get('user_ids', [])

            if not user_ids:
                return make_response(jsonify({"error": "No user IDs provided"}), 400)

            for user_id in user_ids:
                user = Users.query.get(user_id)
                if user:
                    user.role = 'admin'
                else:
                    return make_response(jsonify({"error": f"User with ID {user_id} not found"}), 404)

            db.session.commit()

            return make_response(jsonify({"message": "Users successfully promoted to admin"}), 200)

        except Exception as e:
            return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)