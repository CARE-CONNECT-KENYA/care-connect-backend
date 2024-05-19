from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from urllib.parse import urlparse
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class Facilities(db.Model):
    __tablename__= "facilities"

    facilityId  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facilityphotos = db.Column(db.JSON)
    insurance = db.Column(db.JSON)
    specialties = db.Column(db.JSON)
    ## you can add other filds here 
    

    #foreing keys
    providerID = db.Column(db.Integer, db.ForeignKey('providers.providerID'), nullable=True)

    @validates('facilityphotos')
    def validate_url(self, key, facilityphotos):
        parsed_url = urlparse(facilityphotos)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise AssertionError("Invalid URL. Please provide a valid URL with a scheme (e.g., http, https) and netloc.")
        return facilityphotos

    def __repr__(self):
        return f"Facilities( id ={self.facilityId}, photos={self.facilityphotos} ,insuranc ={self.insurance}, specialty={self.specialties})"






    
