from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from urllib.parse import urlparse
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class IndividualDoctors(db.Model):
    __tablename__='individualDoctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Gender = db.Column(db.String(), nullable=False , unique=False)
    specialties = db.Column(db.JSON)
    LanguagesSpoken= db.Column(db.JSON)
    conditionsTreated = db.Column(db.JSON)
    Procedureperformed= db.Column(db.JSON)
    insurance = db.Column(db.JSON)

    #foreign key
    providerID = db.Column(db.Integer, db.ForeignKey('providers.providerID'), nullable=True)


    def __repr__(self):
        return f"Doctors(id={self.id},Gender={self.Gender},sepcialty={self.specialties},language={self.LanguagesSpoken},codnitions={self.conditionsTreated},procedure={self.Procedureperformed},insurance={self.insurance})"
