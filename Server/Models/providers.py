from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
from urllib.parse import urlparse
from Server.Models.users import Users
from Server.Models.reviews import Review

import re
from app import db

class Providers(db.Model):
    __tablename__= "providers"
    #program  colums
    providerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") , nullable=False)

    #provider details
    bio = db.Column(db.String(250) , nullable=False)
    providerName= db.Column(db.String(50), unique=True , nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    phoneNumber = db.Column(db.Integer(), unique=True , nullable=False)
    workingHours = db.Column(db.String(250), nullable=False)
    profileImage = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255) , nullable=False)
    providerType = db.Column(db.String , nullable=False)
    services = db.Column(db.JSON)

    #relationships 
    user = db.relationship(Users , backref=db.backref('provider' , lazy= True))
    reviews = db.relationship(Review, backref='ngo', lazy=True)


    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Email address must contain the @ symbol.")
        if '.' not in email.split('@')[-1]:
            raise ValueError("Email address must have a valid domain name.")
        return email
    
    @validates('profileImage')
    def validate_url(self, key, profileImage):
        parsed_url = urlparse(profileImage)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise AssertionError("Invalid URL. Please provide a valid URL with a scheme (e.g., http, https) and netloc.")
        return profileImage
    
    @validates('website')
    def validate_url(self, key, website):
        parsed_url = urlparse(website)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise AssertionError("Invalid URL. Please provide a valid URL with a scheme (e.g., http, https) and netloc.")
        return website
    
    @validates('phoneNumber')
    def validate_phoneNumber(self, key, phoneNumber):
        if not phoneNumber.isdigit() and not (phoneNumber.startswith('+') and phoneNumber[1:].isdigit()):
            raise ValueError("Phone number must contain only digits or start with '+' followed by digits.")
        if len(phoneNumber) > 15:
            raise ValueError("Phone number must not exceed 15 characters.")
        return phoneNumber
    
    def __repr__(self):
        return (f"Providers(id={self.providerID}, name={self.providerName}, status={self.status}, "
            f"user_id={self.user_id}, time={self.created_at}, bio={self.bio}, email={self.email}, "
            f"number={self.phoneNumber}, work={self.workingHours}, profilepic={self.profileImage}, "
            f"website={self.website}, location={self.location}, type={self.providerType}, "
            f"services={self.services})")

    
