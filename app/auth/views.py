from flask import render_template, request, redirect, url_for,flash
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models import User
from ..email import welcome_message
from .. import db
from .forms import RegistrationForm, LoginForm


@auth.route('/login', methods = ['GET','POST'])
#def login():
    #login_form = LoginForm()
    #if login_form.validate_on_submit():
        #user = User.query.filter_by(username = login_form.username.data).first()
        #if user != None and user.verify_password(login_form.password.data):
            #login_user(user,login_form.remember.data)
            #return redirect(request.args.get('next') or url_for('main.index'))
        
        #flash('Invalid username or Password')
        
    #title = 'Login'
    #return render_template('login.html', LoginForm = login_form, title=title)
    
def login():
    if request.method == 'POST':
        login_form = request.form
        username = login_form.get('username')
        password = login_form.get('password')
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
#def signup():
    #reg_form = RegistrationForm()
    #if reg_form.validate_on_submit():
        #user = User(email = reg_form.email.data, username = reg_form.username.data, password = reg_form.password.data)
        #db.session.add(user)
        #db.session.commit()
        #welcome_message("Welcome to the Pitch App","email/welcome",user.email,user=user)
        
        #return redirect(url_for('auth.login'))
    
    #title = "Sign Up"
    #return render_template('signup.html', RegistrationForm = reg_form, title=title)
    
def signup():
    if request.method == 'POST':
        reg_form = request.form
        username = reg_form.get("username")
        email = reg_form.get("email")
        password = reg_form.get("password")
        confirm_password = reg_form.get("confirm_password")
        
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