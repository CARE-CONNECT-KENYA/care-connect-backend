import re
from flask import request,jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity
from Server.Models.users import Users
from Server.Models.reviews import Review
from Server.Models.providers import Providers
from app import db

class AddReviews(Resource):
    @jwt_required()
    def post(self, **kwargs):  # Add **kwargs to capture route parameters
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, required=True, help='Rating is required')
        parser.add_argument('text', type=str, required=False, help='Text review')

        args = parser.parse_args()

        current_user_id = get_jwt_identity()
        
        # Check if the user exists
        user = Users.query.get(current_user_id)
        if not user:
            return {'message': 'User not found'}, 404
        

        
        providerID = kwargs.get('providerID')

        provider = Providers.query.get(providerID)
        if not provider:
            return {'message': 'Provider does not exist'}, 404
        

        # Create a new review
        new_review = Review(
            rating=args['rating'],
            text=args.get('text'),  
            user_id=current_user_id,
            providersID=providerID  
        )

        # Add the review to the database
        db.session.add(new_review)
        db.session.commit()

        return {'message': 'Review created successfully'}, 201
             

class GetReviewsForProvider(Resource):
    @jwt_required()
    def get(self, providerID):

        provider = Providers.query.get(providerID)
        if not provider:
            return {'message': 'Provider does not exist'}, 404
        
        reviews = Review.query.filter_by(providerID=providerID).all()
        
        reviews_list=[{
            "id": review.id,
            "rating": review.rating,
            "text":review.text,
            "providerID": review.providerID
        } for review in reviews]

        return {f"Revies for provider": reviews_list}

class GetAllReviews(Resource):
    pass
        


class CalculateAvargeRatingForProvider(Resource):
    def get(self,providerID):
        provider = Providers.query.get(providerID)
        if not provider:
            return {"provider does not exist"}, 404
        
        avaragerating= db.session.query(db.func.avg(Review.rating)).filter_by(providerID=providerID).scalar()
        return {"avrage rating is ": avaragerating} , 200

