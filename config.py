import os

class Config:
    debug = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLAlchemy_DATABASE_URI = 'postgresql+psycopg2://oscar:codingstudent@localhost/pitchapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oscar:codingstudent@localhost/pitchapp'
    
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oscar:codingstudent@localhost/pitchapp'
    
    DEBUG = True
    ENV = 'development'
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}