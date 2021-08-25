from flask import render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from .. import db
from . import main
from .forms import PitchForm, CommentForm
from ..models import User,Pitch,Comment
import datetime

@main.route('/')
def index():
    pitches = Pitch.query.all()

    title = "Home"
    return render_template('index.html', pitches=pitches, title=title, id=id)


@main.route('/pitch/<int:id>', methods = ['POST','GET'])
@login_required
def pitches(id):
    pitch = Pitch.get_pitch(id)

    if request.args.get("upvote"):
        pitch.upvotes = pitch.upvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("downvote"):
        pitch.downvotes = pitch.downvotes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches_count = Pitch.count_pitches(uname)

    if user is None:
        abort(404)

    title = "User"
    return render_template("profile.html", user = user, pitches=pitches, title=title)


@main.route('/new_pitch', methods = ['POST','GET'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.pitch.data

        new_pitch = Pitch(title=title,pitch=pitch,user=current_user)

        new_pitch.save_pitch()
        return redirect(url_for('main.index'))
        
    title = 'New Pitch'
    return render_template('new_pitch.html', pitch_form=pitch_form, title=title)


@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)

    return render_template("profile/pitches.html", user=user,pitches=pitches,pitches_count=pitches_count)


@main.route('/pitches/all_pitches')
def all_pitches(id):

    pitches = Pitch.get_pitches('id')

    return render_template("all_pitches.html", pitches = pitches)