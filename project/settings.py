import os

SECRET_KEY = os.urandom(24)
DEBUG = True
DB_URI = "postgres://twjkqapvdyxjji:79ce19c20132fb550ba22a4becfa49830ea97eedcfde84c429ae3be4416dbded@ec2-54-204-46-236.compute-1.amazonaws.com:5432/d6kav22jlegt9r"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
