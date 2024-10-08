from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify,request,make_response
from Server.Models.providers import Providers
from Server.Models.users import Users
from datetime import datetime
from app import db,mail
from functools import wraps
from flask_mail import Mail, Message

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

# this is a setup for sending emails
def send_email(subject, body, recipient):
    msg = Message(subject, sender=mail.default_sender, recipients=[recipient])
    msg.body = body
    mail.send(msg)
    

class UsersList(Resource):
    @jwt_required()
    @check_role('super_admin')
    def get(self):
        users = Users.query.all()

        all_users = [{
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "password": user.password,
            "role": user.role
        } for user in users]

        return make_response(jsonify(all_users), 200)


class UpdateUserrole(Resource):
    @jwt_required()
    @check_role('super_admin')
    def put(self, user_id):
        # Retrieve the user
        user = Users.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Extract the new role from the request data
        data = request.get_json()
        new_role = data.get('role')

        # Update the user's role if the new role is valid
        if new_role in ['admin', 'user', 'super_admin']:
            user.role = new_role
            db.session.commit()
            return make_response(jsonify({"message": "User role updated successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Invalid role"}), 400)
        
    @check_role('super_admin')    
    def delete(self, user_id):
        user = Users.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"error": "User not found"}, 404

    
class ProvidersList(Resource):
    @jwt_required()
    @check_role('super_admin')
    def get(self):
         
        providers = Providers.query.all()

        all_providers = [{
            
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

        } for provider in providers]
        
        return make_response(jsonify(all_providers))
    
class UnpublishedProviders(Resource):    
    @jwt_required()
    @check_role('super_admin')
    def get(self):

        providers = Providers.query.filter_by(status=False).all()

        notApprovedProviders = [{

            "id": provider.providerID,
            "status": provider.status,
            "reg_date": provider.created_at.strftime('%Y-%m-%d %H:%M:%S'),
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

        } for provider in providers]
        
        return make_response(jsonify(notApprovedProviders), 200)
 
class ApproveProvider(Resource):
    @jwt_required()
    @check_role('super_admin')
    def put(self, providerID):
        # Get the request data
        data = request.get_json()
        new_status = data.get('status')

        # Find the provider with the given providerID
        provider = Providers.query.filter_by(providerID=providerID).first()

        if not provider:
            return make_response(jsonify({"message": "Provider not found"}), 404)

        # Update the provider's status based on the new status
        provider.status = new_status

        # Find the user associated with this provider
        user = Users.query.get(provider.user_id)

        if not user:
            return make_response(jsonify({"message": "User associated with the provider not found"}), 404)

        # Update the user's role based on the provider's new status
        if new_status:
            user.role = 'admin'
        else:
            user.role = 'normal'

        try:
            # Commit the changes to the database
            db.session.commit()

            # Send an email notification to the provider
            self.send_email_notification(provider, new_status)

            return make_response(jsonify({"message": "Provider status and user role updated successfully"}), 200)
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return make_response(jsonify({"message": "An error occurred", "error": str(e)}), 500)

    def send_email_notification(self, provider, new_status):
        # Customize the email subject and body based on the provider's status
        if new_status:
            subject = "Approval Notification: You Have Been Approved!"
            body = f"Dear {provider.providerName},\n\nWe are pleased to inform you that your provider account has been approved. You can now access your dashboard with full privileges.\n\nBest regards,\nYour Company"
        else:
            subject = "Status Update: Your Provider Account"
            body = f"Dear {provider.providerName},\n\nYour provider account status has been updated. Please contact us if you have any questions.\n\nBest regards,\nYour Company"

        # Debugging: Print email details to ensure correct information
        print(f"Sending email to {provider.email} with subject '{subject}'")

        try:
            # Use the provided send_email function to send the email
            send_email(subject, body, provider.email)
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")















