from flask import render_template, request, redirect, url_for,flash
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models import User
from ..email import welcome_message
from .. import db


@auth.route('/login', methods = ['GET','POST'])
    
def login():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        print(username)
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            error = 'Authentication Error. Invalid username.'
            return render_template('login.html', error=error)
        
        has_correct_password = user.verify_password(password)
        print(has_correct_password)
        
        if not has_correct_password:
            error = 'Authentication Error. Invalid password.'
            return render_template('login.html', error=error)
        
        login_user(user)
        return redirect('/')
    
    title = "Login"
    return render_template('login.html', title=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route('/signup', methods = ["GET","POST"])
    
def signup():
    if request.method == 'POST':
        form = request.form
        username = form.get("username")
        email = form.get("email")
        password = form.get("password")
        confirm_password = form.get("confirm_password")
        
        if username is None or password is None or email is None or confirm_password is None:
            error = 'Please fill all the fields.'
            return render_template('signup.html', error=error)
        
        if ' ' in username:
            error = 'Username cannot contain spaces.'
            return render_template('signup.html', error=error)
        
        if password != confirm_password:
            error = "Passwords do not match!"
            return render_template('signup.html', error=error)
        
        else:
            user = User.query.filter_by(username=username).first()
            
            if user is not None:
                error = 'This username is already in use.'
                return render_template('signup.html', error=error)
            
            user = User.query.filter_by(email=email).first()
            if user is not None:
                error = 'This email address is already in use.'
                return render_template('signup.html', error=error)
            
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            
            welcome_message("Welcome to the Pitch App", "email/welcome", user.email, user=user)
            return redirect(url_for('auth.login'))

    title = "Sign Up"
    return render_template('signup.html', title=title)