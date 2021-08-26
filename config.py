import os

class Config:
    DEBUG = True
    SECRET_KEY = 'mysterious_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oscar:123456789@localhost/pitchapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'test.user.python3.6@gmail.com'
    MAIL_PASSWORD = 'codingstudent001'
    
    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    connection = psycopg2.connect(database="gps_heatmap", user="oscar", password="123456789", host="localhost", port=5433)
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oscar:123456789@localhost/pitchapp'
    
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://oscar:123456789@localhost/pitchapp'
    
    DEBUG = True
    ENV = 'development'
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}