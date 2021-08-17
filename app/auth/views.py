from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models import User
from ..email import welcome_message
from .. import db
from .forms import RegistrationForm, LoginForm


@auth.route('/login', methods = ['GET','POST'])
def login():
    l_form = LoginForm()
    if l_form.validate_on_submit():
        user = User.query.filter_by(username = l_form.username.data).first()
        if user != None and user.verify_password(l_form.password.data):
            login_user(user,l_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        
        flash('Invalid username or Password')
        
    title = 'Login'
    return render_template('login.html', LoginForm = l_form, title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route('/signup', methods = ["GET","POST"])
def signup():
    r_form = RegistrationForm()
    if r_form.validate_on_submit():
        user = User(email = r_form.email.data, username = r_form.username.data, password = r_form.password.data)
        db.session.add(user)
        db.session.commit()
        welcome_message("Welcome to the Pitch App","email/welcome",user.email,user=user)
        
        return redirect(url_for('auth.login'))
    
    title = "Sign Up"
    return render_template('signup.html', RegistrationForm = r_form, title=title)