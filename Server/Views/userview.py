from flask_restful import Resource
from Server.Models.users import Users
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,get_current_user,decode_token, JWTManager,get_jwt
from flask import jsonify,request,make_response
from datetime import datetime, timedelta
from flask_jwt_extended import get_current_user
import bcrypt #used to hash passwords
import jwt
from flask_mail import Mail, Message

from functools import wraps
import json


from app import db,jwt,mail



class CountUsers(Resource):
    def get(self):
        users_count = Users.query.count()
        return {"total users": users_count}, 200
    
# this is a setup for sending emails
def send_email(subject, body, recipient):
    msg = Message(subject, sender=mail.default_sender, recipients=[recipient])
    msg.body = body
    mail.send(msg)
    

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

class AddUser(Resource):
    def post(self):
        data = request.get_json()

        if 'fullname' not in data or 'email' not in data or 'password' not in data:
            return {'message': 'Missing fullname, email, or password'}, 400

        fullname = data.get('fullname')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'normal')

        # Check if user already exists
        if Users.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400

        try:
           # Send welcome email first
            subject = "Welcome to Care Connect – Your Gateway to Trusted Medical Professionals"
            body = (
                f"Hello {fullname},\n\n"
                "Welcome to Care Connect! We're thrilled to have you as part of our community. "
                "Whether you're searching for top-rated doctors, specialists, or medical facilities, "
                "Acare Connect is here to make your healthcare journey seamless and stress-free.\n\n"
                "If you have any questions or need assistance, our support team is always here to help. "
                "Simply reply to this email."
            )
            send_email(subject, body, email)

            # If email sending is successful, then validate and add the user
            user = Users(fullname=fullname, email=email, password=password, role=role)
            db.session.add(user)
            db.session.commit()

            return {'message': 'User added successfully'}, 201

        except AssertionError as e:
            # Capture validation errors and return as part of the response
            error_message = str(e)
            error_details = {}

            if "Email" in error_message:
                error_details['email'] = error_message

            if "Password" in error_message:
                error_details['password'] = error_message

            return {'error': error_details}, 400

        except Exception as e:
            print(f"Error adding user: {e}")
            db.session.rollback()
            # If there's an error sending the email or adding the user, return an error response
            if "Invalid email address" in str(e):
                return {'error': 'Failed to send email. Email address is not valid.'}, 400
            return {'error': 'Failed to add user.'}, 500




class UserLogin(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)


        user = Users.query.filter_by(email=email).one_or_none()

        if not user:
            return make_response(jsonify({"error": "User not found. Please check your email."}), 404)

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return make_response(jsonify({"error": "Wrong password"}), 401)
        
        fullname = user.fullname

        # Include the role in the response
        access_token = create_access_token(identity=user, additional_claims={'roles': [user.role]})
        refresh_token = create_refresh_token(identity=user)

        # Include role, access token, and refresh token in the response
        return jsonify({
            "fullname" : fullname,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role
        })

class UserResourcesById(Resource):
    @jwt_required()
    def get(self, user_id):
        user = Users.query.get(user_id)
        if user:
            return {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email,
                "password": user.password,
                "role" : user.role
            }, 200
        else:
            return {"error": "User not found"}, 404
        
    def patch(self, user_id):
 
        user = Users.query.get(user_id)

        if user:
            data = request.get_json()
            fullname = data.get('fullname')
            email = data.get('email')
            

            if fullname:
                user.fullname = fullname
            if email:
                user.email = email
    

            db.session.commit()

            return {'message': 'User updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404
    
        

        

class SendEmail(Resource):
    def post(self):
        try:
            # Hardcoded values
            subject = "Test"
            body = "This is a test email."
            recipient = "erickkirui653@gmail.com"

            if not subject or not body:
                return {"error": "Missing subject or body"}, 400
            
            # Prepare the email
            msg = Message(subject, sender=mail.default_sender, recipients=[recipient])
            msg.body = body
            
            # Send the email
            mail.send(msg)

            return {"message": "Email sent successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
