from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from .models import nob_db, User
from .routes import routes
from .auth import auth
from .admin import admin
import secrets
import os

#The __init.py is like the settings and configuration of the flask app
#create a Flask instance in a function and call it in run.py to run the app
def create_app():
    load_dotenv()
    secret_key0 = secrets.token_hex(16)
    secret_key1 = secrets.token_hex(16)
    app = Flask(__name__) #initialize the flask app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nobdb.db' #configure database
    app.config['API_KEY'] = os.environ.get('API_KEY')  #configure gemini api-key
    app.config['SECRET_KEY'] = secret_key0+secret_key1 #defines a secret key
    app.config['SYSTEM_INSTRUCTION_NOB'] = os.environ.get('SYSTEM_INSTRUCTION_NOB')
    app.config['SYSTEM_INSTRUCTION_DENNIS'] = os.environ.get('SYSTEM_INSTRUCTION_DENNIS')
    
    app.config['MAX_CONTENT_LENGTH'] = 10*1024*1024 #Sets the limit to how large a file can be to be uploaded(10MB)
    app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['.jpg', '.jpeg', '.png','.gif']
    app.config['PROFILE_IMAGE_PATH'] = 'App/static/User_profile_pics'
    app.register_blueprint(routes) #registers the routes from the route.py and the auth.py
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    nob_db.init_app(app) #initializes the database
    # Reference site for authentication: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        nob_db.create_all()
    
    return app