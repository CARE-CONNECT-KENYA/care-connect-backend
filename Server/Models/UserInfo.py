from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class AdditionalUserInfo(db.Model):
    __tablename__= 'userInfo'

    id =  db.Column(db.Integer, primary_key=True, autoincrement=True)
    location  = db.Column(db.String(255) )
    conditions = db.Column(db.JSON)
    insuranceUse = db.Column(db.JSON)
    userType = db.Column(db.String(10))

    #foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") , nullable=False)

    def __repr__(self):
        return f"user(id ={self.id} , location={self.location} , conditions={self.conditions} ,insurance={self.insuranceUse})"
