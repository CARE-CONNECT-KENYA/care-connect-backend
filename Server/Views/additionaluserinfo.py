from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from app import db
from Server.Models.UserInfo import AdditionalUserInfo
from Server.Models.users import Users


class AdditionalUserInfoResource(Resource):
    @jwt_required()
    def post(self):
        # Get the current user's identity
        user_id = get_jwt_identity()

        # Parse the JSON request body
        data = request.get_json()

        # Validate and extract fields from the request data
        location = data.get('location')
        conditions = data.get('conditions')
        insuranceUse = data.get('insuranceUse')
        userType = data.get('userType')

        # Check if additional info already exists for the user
        additional_info = AdditionalUserInfo.query.filter_by(user_id=user_id).first()
        if additional_info:
            return {"error":"user additional info alrady exists"}, 400

        new_info = AdditionalUserInfo(
                user_id=user_id,
                location=location,
                conditions=conditions,
                insuranceUse=insuranceUse,
                userType=userType
            )
        
        db.session.add(new_info)
        db.session.commit()

        return jsonify({'message': 'Additional user info saved successfully'})
    
class USerInfo(Resource):
    @jwt_required()
    def get(self, id):

        additional_info = AdditionalUserInfo.query.get_or_404(id)


        # Return the user's additional info as JSON
        info = {
            "id": additional_info.id,
            "location": additional_info.location,
            "conditions": additional_info.conditions,
            "insurance": additional_info.insuranceUse,
            "userType": additional_info.userType
        }

        return jsonify({"info": info})
    
    @jwt_required()
    def put(self, id):

        userInfo = AdditionalUserInfo.query.get_or_404(id)
        data = request.json

        #update information

        userInfo.location=data.get('location')
        userInfo.conditions=data.get('conditions')
        userInfo.insuranceUse = data.get('insuranceUse')
        userInfo.userType = data.get('userType')

        db.session.commit()

        return {"message": "Information updated succesfully"}, 200

        

    @jwt_required()
    def delete(self,user_id):
        # Get the current user's identity
        user_id = get_jwt_identity()
        

        # Find the user's additional info
        additional_info = AdditionalUserInfo.query.filter_by(user_id=user_id).first()
        if not additional_info:
            return {"error": "User additional info not found"}, 404

        db.session.delete(additional_info)
        db.session.commit()

        return jsonify({'message': 'Additional user info deleted successfully'})