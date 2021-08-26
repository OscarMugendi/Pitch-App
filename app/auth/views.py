from flask import render_template, request, redirect, url_for,flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app.models import User
from ..email import welcome_message
from .. import db
from .forms import RegistrationForm,LoginForm
from .. import main


@auth.route('/login', methods = ['GET','POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()
        
        if user != None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            
            return redirect(request.args.get('next') or url_for('main.index'))
        
        flash('Authentication Error!')
        
    title = "Login"
    return render_template('login.html', login_form = login_form, title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route('/signup', methods = ["GET","POST"])
def signup():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(
                    email = form.email.data,
                    username = form.username.data,
                    password = form.password.data
                )
        
        db.session.add(user)
        db.session.commit()

        welcome_message("Welcome to the Pitch Community!","email/welcome",user.email,user=user)
        
        return redirect(url_for('auth.login'))
    
    title = "Signup"
    return render_template('signup.html', form = form, title=title)