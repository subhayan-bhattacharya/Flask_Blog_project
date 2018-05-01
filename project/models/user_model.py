from project import db
from flask import session


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(35),unique=True)
    password = db.Column(db.String(60))
    is_author = db.Column(db.BOOLEAN)

    #Relationship with posts(One to many relationship). One user can have many posts
    posts = db.relationship('Post',backref='user',lazy='dynamic')
    #Relationship with comments(One to many relationship).One user could have made many comments
    comments = db.relationship('Comment',backref='user',lazy='dynamic')

    @classmethod
    def get_current_user(cls):
        user_result = None
        if 'username' in session:
            user = session['username']
            user_result = cls.get_user_by_username(username=user)
        return user_result

    @classmethod
    def get_user_by_username(cls,username):
        user = None
        user = cls.query.filter_by(username=username).first()
        return user
       
    @classmethod
    def get_by_id(cls,id):
        user = None
        user = cls.query.filter_by(id=id).first()
        return user

    @classmethod
    def get_user_by_email(cls,email):
        user = None
        user = cls.query.filter_by(email=email).first()
        return user

    @classmethod
    def get_user_by_id(cls,id):
        user = cls.query.filter_by(id=id).first()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        if self.id:
            db.session.commit()
            return True
        else:
            db.session.rollback()
            return False
