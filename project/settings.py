import os

SECRET_KEY = os.urandom(24)
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = True
