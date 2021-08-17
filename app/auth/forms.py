from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Required,Email,EqualTo

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[Required(),Email()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('confirm_password',message = 'Passwords must match.')])
    confirm_password = PasswordField('Confirm Password',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("This email address is already in use.")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("This username is already in use.")