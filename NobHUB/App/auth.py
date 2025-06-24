from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import nob_db
from .models import User, Contacts, Messages
from .NOB_AI import NOB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

#The auth.py defines the routes and logic for registration and authentication of users
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_password = request.form.get('password0')
        confirm_user_password = request.form.get('password1')
        if user_password!= confirm_user_password:
            flash("Passwords must be same")
            return redirect(url_for('auth.signup'))
        elif len(user_password)<=5:
            flash("Passwords must be greater than 5 digits")
            return redirect(url_for('auth.signup'))
        
        username= request.form.get('username')
        user_email= request.form.get('user_email')
        user_number= request.form.get('number')
    
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
        nob_ai_exists = User.query.filter_by(username='N.O.B').first()
        dennis_ai_exists = User.query.filter_by(username='dennis').first()
        nob_ai = User(username='N.O.B', user_number='0000001', user_email='nob@ai.com', user_password_hash='-', user_image_path='static/images/defaultimg.jpg')
        dennis_ai = User(username='Dennis', user_number='0000002', user_email='dennis@ai.com', user_password_hash='-', user_image_path='static/images/defaultimg.jpg')
       
        
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
    else:
        return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    user_password = request.form.get('password0')

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Username is does not exist!')

    if not user or not check_password_hash(user.user_password_hash, user_password):
        flash('Password is incorrect!')
        return redirect(url_for('auth.login'))
    login_user(user)
    #return NOB(f"Hello I am {username}")
    return redirect('/home')
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))