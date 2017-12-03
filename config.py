import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    CLIENT_ID = ('4776864356-jofjojmr70la6q8f67napv6qjenlhnal.apps.googleusercontent.com')
    CLIENT_SECRET = 'vmZ1nMyaFP7-PgLkPgO136_q'
    REDIRECT_URI = 'http://localhost:5000/gCallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']


class Config:
    APP_NAME = "IIITA Hotel Reservation"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://diksha:diksha@127.0.0.1:5432/college'


class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://diksha:diksha@127.0.0.1:5432/college'


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}