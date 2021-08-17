from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models import User
from ..email import welcome_message
from .. import db
from .forms import RegistrationForm, LoginForm


@auth.route('/login', methods = ['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user != None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        
        flash('Invalid username or Password')
        
    title = 'Login'
    return render_template('login.html', LoginForm = login_form, title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route('/signup', methods = ["GET","POST"])
def signup():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(email = reg_form.email.data, username = reg_form.username.data, password = reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        welcome_message("Welcome to the Pitch App","email/welcome",user.email,user=user)
        
        return redirect(url_for('auth.login'))
    
    title = "Sign Up"
    return render_template('signup.html', RegistrationForm = reg_form, title=title)