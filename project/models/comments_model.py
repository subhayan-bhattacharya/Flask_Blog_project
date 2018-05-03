from project import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commenter_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    comment = db.Column(db.TEXT)
    date = db.Column(db.DateTime)

    def __init__(self,commenter_id,post_id,comment):
        self.post_id = post_id
        self.commenter_id = commenter_id
        self.comment = comment
        self.date = datetime.utcnow()

    @classmethod
    def get_all_comments(cls,post_id,page):
        comments = []
        COMMENTS_PER_PAGE = 2
        comments = cls.query.filter_by(post_id=post_id).order_by(cls.date.desc()).paginate(page,COMMENTS_PER_PAGE,False)
        return comments
        
    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        if self.id:
            db.session.commit()
            return True
        else:
            db.session.rollback()
            return False
        
