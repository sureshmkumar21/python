
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET KEY'
    CSRF_SESSION_KEY = "secret"
    CSRF_ENABLED     = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'mymail@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopementConfig(BaseConfig):
    DEBUG = True
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    REDIRECT_URI = 'http://localhost:7001/callback'
    CLIENT_ID = "RC225"
    CLIENT_SECRET = "weAIZ6GmORRDKYA5IWgs3UjRFFZS6k0tKm2LYmxVvZN5yb5RVTVApPmq3bNVDqi8"
    AUTHORIZATION_BASE_URL = 'https://ant.aliceblueonline.com/oauth2/auth'
    TOKEN_URL = 'https://ant.aliceblueonline.com/oauth2/token'

