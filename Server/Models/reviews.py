from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class Review(db.Model):
    __tablename__='reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    #Foreign keys column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    providersID = db.Column(db.Integer, db.ForeignKey('providers.providerID'), nullable=True)

    def __repr__(self):
        return f"Review(id={self.id}, rating={self.rating}, text='{self.text}')"


