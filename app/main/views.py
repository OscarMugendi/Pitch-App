from flask import render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from .. import db
from . import main
from .forms import PitchForm, CommentForm
from ..models import User,Pitch,Comment,Upvote,Downvote


@main.route('/')

def index():
    pitches = Pitch.query.all()

    title = "Home"
    return render_template('index.html', pitches=pitches, title=title)


@main.route('/pitches', methods = ['POST','GET'])

@login_required
def pitches():
    pitches = Pitch.query.all()
    upvotes = Upvote.query.all()
    downvotes = Downvote.query.all()
    user = current_user

    title = "Home - User"
    return render_template('index.html', pitches=pitches, upvotes=upvotes, downvotes=downvotes, user=user, title=title)


@main.route('/user/<uname>', methods = ['POST','GET'])

@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    pitches = Pitch.query.filter_by(user_id = user_id).all()

    if user is None:
        abort(404)

    title = "User"
    return render_template("profile.html", user = user, pitches=pitches, title=title)


@main.route('/new_pitch', methods = ['POST','GET'])

@login_required
def new_pitch():
    form = PitchForm()
    
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        user_id = current_user
        new_pitch_object = Pitch(pitch=pitch,user_id=current_user.get_current_object().id,title=title)
        new_pitch_object.save_pitch()
        return redirect(url_for('main.index'))
        
    return render_template('new_pitch.html', form = form,user_id=current_user)


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])

@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    user = User.query.all()
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        
        new_comment.save_comment()
        return redirect(url_for('main.comment', pitch_id = pitch_id,user_id=user_id))
    
    title = "Comment"
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments, user=user, title=title)


@main.route('/upvote/<int:id>',methods = ['POST','GET'])

@login_required
def upvote(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        
        if valid_string == to_str:
            
            return redirect(url_for('main.index',id=id))
        
        else:           
            continue
        
    new_upvote = Upvote(user = current_user, pitch_id=id)
    new_upvote.save()
    
    return redirect(url_for('main.index',id=id))


@main.route('/downvote/<int:id>',methods = ['POST','GET'])

@login_required
def downvote(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        
        if valid_string == to_str:
            
            return redirect(url_for('main.index',id=id))
        
        else:
            continue
        
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save()
    
    return redirect(url_for('main.index',id = id))
