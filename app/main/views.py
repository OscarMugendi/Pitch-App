from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .forms import PitchForm, CommentForm
from ..models import User


@main.route('/')
def index():
    #posts = Pitch.query.all()
    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile.html", user = user)