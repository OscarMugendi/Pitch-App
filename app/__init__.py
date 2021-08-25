from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config_options

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    
    login_manager.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    
    return app