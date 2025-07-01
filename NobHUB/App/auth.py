from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import nob_db
from .models import User, Contacts, Messages
from .NOB_AI import NOB
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

#The auth.py defines the routes and logic for registration and authentication of users
auth = Blueprint('auth', __name__)
#Flask WTF
class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username is required")])
    email = StringField("Email", validators=[DataRequired(message="Email is required"),Email(message="Enter a valid email address")])
    phoneNumber = StringField("Phone Number", validators=[DataRequired(message="Phone Number is required")])
    password0 = PasswordField("Password", validators=[DataRequired(message="Password is required"),  Length(min=8, message="Passwords must be greater than 8 digits")])
    password1 = PasswordField("Password", validators=[DataRequired(message="Password is required"),EqualTo('password0', message="Passwords must be same")])
    submit = SubmitField("Save")
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username is required")])
    user_password = PasswordField("Password", validators=[DataRequired(message="Password is required")])
    submit = SubmitField("GO")
@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():

            user_password = signup_form.password0.data
            confirm_user_password = signup_form.password1.data
            # if user_password!= confirm_user_password:
            #     flash("Passwords must be same")
            #     return redirect(url_for('auth.signup'))
            # elif len(user_password)<=5:
            #     flash("Passwords must be greater than 5 digits")
            #     return redirect(url_for('auth.signup'))
            
            username= signup_form.username.data
            user_email= signup_form.email.data
            user_number= signup_form.phoneNumber.data

            user = User.query.filter_by(username=username).first()
            email = User.query.filter_by(user_email=user_email).first()

            if user:
                flash('Username already exist!')
                return redirect(url_for('auth.signup'))
            if email:
                flash('Email already registered!')
                return redirect(url_for('auth.signup'))

            user_password_hashed = generate_password_hash(user_password, method='pbkdf2:sha256')
            new_user = User(username=username, user_email=user_email, user_number=user_number,user_password_hash=user_password_hashed,user_image_path='static/images/defaultimg.jpg')
            
            
            try:
                nob_db.session.add(new_user)
                nob_ai_exists = User.query.filter_by(username='N.O.B').first()
                dennis_ai_exists = User.query.filter_by(username='Dennis').first()
                if not nob_ai_exists:
                    nob_ai = User(username='N.O.B', user_number='0000001', user_email='nob@ai.com', user_password_hash='-', user_image_path='static/images/defaultimg.jpg')
                    nob_db.session.add(nob_ai)
                if not dennis_ai_exists:
                    dennis_ai = User(username='Dennis', user_number='0000002', user_email='dennis@ai.com', user_password_hash='-', user_image_path='static/images/defaultimg.jpg')
                    nob_db.session.add(dennis_ai)
                
            
                nob_db.session.commit()
                return redirect('/login')
            except Exception as e:
                nob_db.session.rollback()
                print(e)
                return "Error 101: Failed to add user. Please try again!"    
    
    return render_template('signup.html', signup_form=signup_form)


@auth.route('/login', methods=['GET','POST'])
def login():
    # username = request.form.get('username')
    # user_password = request.form.get('password0')
    login_form = LoginForm()
    username = None
    user_password = None
    if login_form.validate_on_submit():
        username = login_form.username.data
        user_password = login_form.user_password.data
    
        user_or_email = User.query.filter(or_(User.username==username, User.user_email==username)).first()
        
        if not user_or_email:
            flash('Username/Email does not exist!')
            return redirect(url_for('auth.login'))

        if not user_or_email or not check_password_hash(user_or_email.user_password_hash, user_password):
            flash('Password is incorrect!')
            return redirect(url_for('auth.login'))
        login_user(user_or_email)
        #return NOB(f"Hello I am {username}")
        return redirect('/home')
    return render_template('login.html',login_form=login_form)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))