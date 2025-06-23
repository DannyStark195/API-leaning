from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin #UserMixin will add Flask-Login attributes to the model so that Flask-Login will be able to work with it.
from datetime import datetime

# The models.py define the structure of the database. 
# The Users class defines the users table for all users
# The Contacts class defines the contacts table for all and each user's contact
# The Messages class defines the messages table for all each user and their contacts
# Reference site for authentication: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

nob_db = SQLAlchemy()

class User(UserMixin, nob_db.Model):
    id = nob_db.Column(nob_db.Integer, primary_key=True)
    username = nob_db.Column(nob_db.String(20), nullable=False)
    user_number = nob_db.Column(nob_db.String(200), nullable=False)
    user_email = nob_db.Column(nob_db.String(100), nullable=False)
    user_password_hash = nob_db.Column(nob_db.String(200), nullable=False)
    user_image_path =  nob_db.Column(nob_db.String(200), nullable=False)
    contacts = nob_db.relationship('Contacts', backref='user', lazy=True) # A two way relationship between the user and their contacts and messages
    messages = nob_db.relationship('Messages', backref='user', lazy=True)
class Contacts(nob_db.Model):
    id = nob_db.Column(nob_db.Integer, primary_key=True)
    user_id = nob_db.Column(nob_db.Integer, nob_db.ForeignKey('user.id'), nullable=False)
    contact_id = nob_db.Column(nob_db.Integer, nob_db.ForeignKey('contacts.id'), nullable=False)  # <-- Add this
    # contact_id = nob_db.Column(nob_db.Integer, nullable=False)
    contact_name = nob_db.Column(nob_db.String(20), nullable=False)
    contact_number = nob_db.Column(nob_db.String(200), nullable=False)
    contact_image_path =  nob_db.Column(nob_db.String(200), nullable=False)
    messages = nob_db.relationship('Messages', backref='contact', lazy=True)
class Messages(nob_db.Model):
    id = nob_db.Column(nob_db.Integer, primary_key=True)
    user_id = nob_db.Column(nob_db.Integer, nob_db.ForeignKey('user.id'), nullable=False)
    contact_id = nob_db.Column(nob_db.Integer, nob_db.ForeignKey('contacts.id'), nullable=False)
    message = nob_db.Column(nob_db.Text, nullable=False)
    # user_message = nob_db.Column(nob_db.Text, nullable=False)
    # contact_message = nob_db.Column(nob_db.Text, nullable=False)
    time = nob_db.Column(nob_db.DateTime, default=datetime.utcnow)

