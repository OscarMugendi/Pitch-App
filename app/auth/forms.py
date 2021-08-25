from flask_wtf import FlaskForm
from wtforms import ValidationError,StringField,PasswordField,SubmitField,BooleanField,TextAreaField,IntegerField
from wtforms.validators import Required,Email,EqualTo
from wtforms.fields.core import IntegerField,StringField,BooleanField
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Continue')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(),Email()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Password Mismatch')])
    password_confirm = PasswordField('Confirm Password',validators = [Required()])
    submit = SubmitField('Create New Account')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("This email address is already in use.")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("This username is already in use.")
