import os

SECRET_KEY = os.urandom(24)
DEBUG = True
DB_URI = "sqlite:///data.db"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = "static\images"
