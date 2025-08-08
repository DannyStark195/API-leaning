from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_from_directory, session
from .models import nob_db
from .models import User, Contacts, Messages
from .NOB_AI import NOB
from .events import socketio
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_login import login_user, logout_user, login_required
from authlib.integrations.flask_client import OAuth
from .myWTF_Forms import SignupForm, LoginForm
from . import oauth
import secrets
import os

#The auth.py defines the routes and logic for registration and authentication of users
auth = Blueprint('auth', __name__)
#Flask WTF

#Google OAUth login
# CLIENT_ID = current_app.config['CLIENT_ID']
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

def init_google_oauth(client_id, client_secret):
    """Initializes the Google OAuth client."""
    global google
    google = oauth.register(
        name='google',
        client_id=client_id,
        client_secret=client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={"scope":"openid profile email"}
    )

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
            
            #Added and used lask wtf for form validation
            username= signup_form.username.data
            user_email= signup_form.email.data
            user_number= signup_form.phoneNumber.data
            
            user_profile_pic = signup_form.profile_pic.data
            if user_profile_pic:
                imagename= secure_filename(user_profile_pic.filename)
                user_image_path = os.path.join(current_app.config['PROFILE_IMAGE_PATH'], imagename)
                user_profile_pic.save(os.path.join('App/static',user_image_path))
            else:
                user_image_path= os.path.join(current_app.config['PROFILE_IMAGE_PATH'], 'defaultimg.jpg')
            user = User.query.filter_by(username=username).first()
            email = User.query.filter_by(user_email=user_email).first()

            if user:
                flash('Username already exist!')
                return redirect(url_for('auth.signup'))
            if email:
                flash('Email already registered!')
                return redirect(url_for('auth.signup'))

            user_password_hashed = generate_password_hash(user_password, method='pbkdf2:sha256')
            new_user = User(username=username, user_email=user_email, user_number=user_number,user_password_hash=user_password_hashed,user_image_path=user_image_path)
            
            
            try:
                nob_db.session.add(new_user)
                nob_ai_exists = User.query.filter_by(username='N.O.B').first()
                dennis_ai_exists = User.query.filter_by(username='Dennis').first()
                if not nob_ai_exists:
                    nob_ai = User(username='N.O.B', user_number='0000001', user_email='nob@ai.com', user_password_hash='-', user_image_path=os.path.join(current_app.config['PROFILE_IMAGE_PATH'], 'defaultimg.jpg'))
                    nob_db.session.add(nob_ai)
                if not dennis_ai_exists:
                    dennis_ai = User(username='Dennis', user_number='0000002', user_email='dennis@ai.com', user_password_hash='-', user_image_path=os.path.join(current_app.config['PROFILE_IMAGE_PATH'], 'defaultimg.jpg'))
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
        # socket.emit('join_global_chat', {'user':user_or_emial'})
        # #return NOB(f"Hello I am {username}")
        
        return redirect(url_for('routes.home'))
    return render_template('login.html',login_form=login_form)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Google login
@auth.route('/login/google')
def login_google():
    try: 
        redirect_url = url_for('auth.authorize_google', _external=True)
        print("YOO NO error")
        return google.authorize_redirect(
            redirect_url,
            prompt= 'select_account',
        )
        print("YOO error")
    except Exception as e:
        # This will now print the exact error message
        print(f"Error during login: {e}")
        return "An error occurred. Check the server logs for details.", 500
@auth.route('/authorize/google')
def authorize_google():

    try:
        token = google.authorize_access_token()
        user_info_endpoint = google.server_metadata['userinfo_endpoint']
        resp = google.get(user_info_endpoint)
        user_info = resp.json()

        username_split = user_info['email'].split('@')
        username = '@'.join(username_split[:-1])
        print(username)
        user_email = user_info['email']
        print(user_email)
        user_or_email = User.query.filter_by(user_email=user_email).first()
        user_image_path= os.path.join(current_app.config['PROFILE_IMAGE_PATH'], 'defaultimg.jpg')
        if not user_or_email:
            new_user = User(username=username, user_email=user_email, user_number=f'{secrets.token_hex(16)}',user_password_hash=f'{secrets.token_hex(16)}',user_image_path=user_image_path)
                
            nob_db.session.add(new_user)
                    
            nob_db.session.commit()
        login_user(user_or_email)
                 
    except Exception as e:
                nob_db.session.rollback()
                print(e)
                return "Error 101: Failed to add user. Please try again!"    
    session['oauth_token'] = token
    login_user(user_or_email)
    return redirect(url_for('routes.home'))

    
    







# Authorize for google



@auth.route('/profile_pic', methods=['GET'])
def profile_pic():
    return render_template('profile_pic.html')

@auth.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    try:
        file = request.files['profilePic']
    except RequestEntityTooLarge:
        flash("File is larger than 10MB limt")
        return redirect(url_for('auth.profile_pic'))
    extension = os.path.splitext(file.filename)[1]
    if file:
        if extension not in current_app.config['ALLOWED_IMAGE_EXTENSIONS']:
            flash('File is not an image')
            return redirect(url_for('auth.profile_pic'))
        image_name = secure_filename(file.filename)
        imgpath = os.path.join(current_app.config['PROFILE_IMAGE_PATH'], image_name)
        file.save(imgpath)
        
        return render_template('profile_pic.html', image_name=image_name)

    return redirect('/profile_pic')

# @auth.route('/serve-images/<filename>', methods=['GET'])
# def serve_image(filename):
   
#     return send_from_directory(current_app.config['PROFILE_IMAGE_PATH'], filename)

