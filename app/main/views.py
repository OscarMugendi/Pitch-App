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
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch_object = Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_p()
        return redirect(url_for('main.index'))
        
    return render_template('new_pitch.html', form = form)


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])

@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)
        
        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments)


@main.route('/like/<int:id>',methods = ['POST','GET'])

@login_required
def like(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
        
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save_upvote()
    return redirect(url_for('main.index',id=id))


@main.route('/dislike/<int:id>',methods = ['POST','GET'])

@login_required
def dislike(id):
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
    new_downvote.save_downvote()
    return redirect(url_for('main.index',id = id))