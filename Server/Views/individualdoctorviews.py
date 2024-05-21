from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from Server.Models.IndividualDoctors import IndividualDoctors
from Server.Models.providers import Providers
from app import db

class AddIndividualDoctor(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()  # Get the current user's ID


            # Extract data from the request payload
            data = request.json
            gender = data.get('Gender')

            if gender.lower() not in ["male", "female"]:
                return {"error": "Gender must be either 'Male' or 'Female'."}, 400
            
            specialties = data.get('specialties')
            languages_spoken = data.get('LanguagesSpoken')
            conditions_treated = data.get('conditionsTreated')
            procedures_performed = data.get('Procedureperformed')
            insurance = data.get('insurance')

            # Validate the data if necessary

            # Find the providerID associated with the current user
            provider = Providers.query.filter_by(user_id=current_user_id).first()
            if not provider:
                return {"error": "Provider not found for the current user."}, 404

            provider_id = provider.providerID

            # Check if provider ID already exists
            existing_doctor = IndividualDoctors.query.filter_by(providerID=provider_id).first()
            if existing_doctor:
                return {"error": "Individual doctor with the provider ID has existing details"}, 400

            # Create a new IndividualDoctor instance
            new_doctor = IndividualDoctors(
                Gender=gender,
                specialties=specialties,
                LanguagesSpoken=languages_spoken,
                conditionsTreated=conditions_treated,
                Procedureperformed=procedures_performed,
                insurance=insurance,
                providerID=provider_id
            )

            # Add the new doctor to the database
            db.session.add(new_doctor)
            db.session.commit()

            return {"message": "Individual doctor added successfully."}, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        
class GetIndividualDoctorDetails(Resource):
    @jwt_required()

    def get(self, providerID):
        
        provider = Providers.query.get(providerID)
        if not provider:
            return {"message": f"Provider {providerID} does not exist"}, 404

        doctors = IndividualDoctors.query.filter_by(providerID=providerID).all()

        doctors_list = [{
            "id": doctor.id,
            "gender": doctor.Gender,
            "specialties": doctor.specialties,
            "languagesSpoken": doctor.LanguagesSpoken,
            "conditionsTreated": doctor.conditionsTreated,
            "procedurePerformed": doctor.Procedureperformed,
            "insurance": doctor.insurance,
            "providerId": doctor.providerID
        } for doctor in doctors]

        return {"doctor_info": doctors_list}, 200





