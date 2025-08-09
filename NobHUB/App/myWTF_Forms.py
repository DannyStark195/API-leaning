from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username is required")])
    email = StringField("Email", validators=[DataRequired(message="Email is required"),Email(message="Enter a valid email address")])
    phoneNumber = StringField("Phone Number", validators=[DataRequired(message="Phone Number is required")])
    password0 = PasswordField("Password", validators=[DataRequired(message="Password is required"),  Length(min=8, message="Passwords must be greater than 8 digits")])
    password1 = PasswordField("Password", validators=[DataRequired(message="Password is required"),EqualTo('password0', message="Passwords must be same")])
    profile_pic = FileField("Profile",validators=[FileAllowed( ['jpg', 'jpeg', 'png','gif'], message='Please Upload an image!')])
    submit = SubmitField("Save")

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(message="Username is required")])
    user_password = PasswordField("Password", validators=[DataRequired(message="Password is required")])
    submit = SubmitField("GO")

class EditForm(FlaskForm):
    username = StringField('Username')
    email = StringField("Email", validators=[Optional(),Email(message="Enter a valid email")])
    phoneNumber = StringField('Phone Number')
    profile_pic = FileField("Profile", validators=[FileAllowed(['jpg', 'jpeg', 'png','gif'], message='Please Upload an image')])
    edit = SubmitField("CHANGE")

class ResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("Email is required"),Email(message="Enter a valid email")])
    password0 = PasswordField("Password", validators=[DataRequired(message="Password is required"),  Length(min=8, message="Passwords must be greater than 8 digits")])
    password1 = PasswordField("Password", validators=[DataRequired(message="Password is required"),EqualTo('password0', message="Passwords must be same")])
    request = SubmitField("Request Reset")
    reset = SubmitField('Reset Password')
    