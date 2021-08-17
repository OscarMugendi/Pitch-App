from flask_wtf import FlaskForm
from wtforms import  StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    post = TextAreaField('Pitch', validators=[Required()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Post Comment')


class Vote(FlaskForm):
    submit = SelectField('Like')
