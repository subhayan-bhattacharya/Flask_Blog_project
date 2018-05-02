from flask import Flask,redirect,url_for
from os import urandom
from flaskext.markdown import Markdown
from project.db import db
app = Flask(__name__)
app.config.from_object('project.settings')

db.init_app(app)
Markdown(app)

from project.posts.views import posts_blueprint
from project.users.views import users_blueprint
from project.comments.views import comments_blueprint

app.register_blueprint(posts_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(comments_blueprint)

@app.before_first_request
def init_app():
    db.create_all()
