from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
from Server.Models.reviews import Review
from app import db
import re #used for validation
import bcrypt #used to hash passwords


class Users(db.Model):
    __tablename__ = "users"
    
    #table colums
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    role = db.Column(db.String, nullable=False, default='normal')

    #ralationships 
    reviews = db.relationship(Review, backref='user', lazy=True)

    # Data validation
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Email address must contain the @ symbol."
        assert '.' in email.split('@')[-1], "Email address must have a valid domain name."
        return email


    @validates('role')
    def validate_role(self, key, role):
        valid_roles = ['normal', 'super_admin', 'admin']
        assert role in valid_roles, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        return role


    @validates('password')
    def validate_password(self, key, password):
        error_messages = []

        if len(password) < 8:
            error_messages.append("Password must be at least 8 characters long.")

        if not any(char.isupper() for char in password):
            error_messages.append("Password must contain at least one capital letter.")

        if not any(char.isdigit() for char in password):
            error_messages.append("Password must contain at least one number.")

        if not re.search(r'[!@#$%^&*()-_=+{};:,<.>]', password):
            error_messages.append("Password must contain at least one symbol.")

        if error_messages:
            raise AssertionError(" ".join(error_messages))

        return self.hash_password(password)
    

    def hash_password(self, password):
        # Hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def has_role(self, role):
        return self.role == role

    def __repr__(self):
        return f"User(id={self.id}, username='{self.fullname}',email='{self.email}', role='{self.role}',password='{self.password}')"

    

