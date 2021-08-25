from flask_wtf import FlaskForm
from wtforms import  StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    pitch = TextAreaField('Your Pitch', validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a Comment', validators=[Required()])
    submit = SubmitField('Submit')