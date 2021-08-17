from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from . import main
from .forms import PitchForm, CommentForm
from ..models import User,Pitch,Comment,Upvote,Downvote


@main.route('/')
def index():
    pitches = Pitch.query.all()
    return render_template('index.html', pitches=pitches)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile.html", user = user)


@main.route('/new_pitch', methods = ['POST','GET'])

@login_required
def new_pitch():
    form = PitchForm()
    
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        user_id = current_user._get_current_object().id
        new_pitch_object = Pitch(pitch=pitch,user_id=user_id,title=title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))
        
    return render_template('new_pitch.html', form = form)


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])

@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    user = User.query.all()
    comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id,user_id=user_id))
    
    title = "Comment"
    return render_template('comment.html', form =form, pitch = pitch,comments=comments, user=user, title=title)


@main.route('/like/<int:id>',methods = ['POST','GET'])

@login_required
def upvote(id):
    pitch = Pitch.query.get(id)
    new_upvote = Upvote(pitch=pitch, upvote=1)
    new_upvote.save()
    return redirect(url_for('main.pitches'))


@main.route('/dislike/<int:id>',methods = ['POST','GET'])

@login_required
def downvote(id):
    pitch = Pitch.query.get(id)
    new_downvote = Downvote(pitch=pitch, downvote=1)
    new_downvote.save()
    return redirect(url_for('main.pitches'))


@main.route('/user')
@login_required
def user():
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        return ('not found')
    
    title = "User"
    return render_template('profile.html', user=user, title=title)