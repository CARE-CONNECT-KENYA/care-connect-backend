from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from Server.Models.providers import Providers
from Server.Models.facilities import Facilities
from Server.Models.IndividualDoctors import IndividualDoctors
from app import db

class AddFacilities(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()

            data = request.json
            facilityphotos = data.get("facilityphotos")
            insurance = data.get("insurance")
            specialties = data.get("specialties")

            # Find the providerID associated with the current user
            provider = Providers.query.filter_by(user_id=current_user_id).first()
            if not provider:
                return {"error": "Provider not found for the current user."}, 404

            provider_id = provider.providerID
            providerType = provider.providerType

            # Check if the provider type is "Facility"
            if providerType != "Facility":
                return {"error": "Provider type must be a Facility."}, 400

            # Check if user ID has facility
            existing_facility = Facilities.query.filter_by(providerID=provider_id).first()
            if existing_facility:
                return {"error": "Facility with the provider ID has existing details"}, 400

            new_facility = Facilities(
                facilityphotos=facilityphotos,
                insurance=insurance,
                specialties=specialties,
                providerID=provider_id
            )

            db.session.add(new_facility)
            db.session.commit()

            return {"message": "Facility added successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


class GetFacilityForProvider(Resource):

    @jwt_required()
    def get(self, providerID):
        provider = Providers.query.get(providerID)
        if not provider:
            return {"message": f"Provider {providerID} does not exist"}, 404
        
        facilities = Facilities.query.filter_by(providerID=providerID).all()

        facility_list =[{
            "id": facility.facilityId,
            "facilityphotos": facility.facilityphotos,
            "insurance":facility.insurance,
            "specialties":facility.specialties

        } for facility in facilities]

        return {"facility": facility_list}, 200
