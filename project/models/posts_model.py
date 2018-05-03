from project import db
from datetime import datetime
from .user_model import User
from .tag_model import Tag,assoc_table

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.TEXT)
    slug = db.Column(db.String(256),unique=True)
    date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    is_live = db.Column(db.BOOLEAN)

    #Relationship with comments(One to many relationship). One post can have many comments
    #comments = db.relationship('Comment', backref='post', lazy='dynamic',order_by="Comment.date")
    #Relationship with tags(Many to many relationship).One post can have many tags and one tag can be associated with many posts
    tags = db.relationship('Tag',secondary='posts_tags',backref='posts', lazy='dynamic')

    def __init__(self,title,body,author_id,is_live,slug=None):
        self.title = title
        self.body = body
        self.slug = slug
        self.date = datetime.utcnow()
        self.author_id = author_id
        self.is_live = is_live

    @classmethod
    def get_all_posts(cls,page):
        added_posts = []
        POSTS_PER_PAGE = 2
        added_posts = cls.query.filter_by(is_live=True).order_by(cls.date.desc()).paginate(page,POSTS_PER_PAGE,False)
        return added_posts
        
    @classmethod
    def get_all_author_posts(cls,id,page):
        all_posts = []
        POSTS_PER_PAGE = 2
        all_posts = cls.query.filter_by(author_id=id).order_by(cls.date.desc()).paginate(page,POSTS_PER_PAGE,False)
        return all_posts
        
    @classmethod
    def get_post_by_id(cls,id):
        post = None
        post = cls.query.filter_by(id=id).first()
        return post
    

    @classmethod
    def get_post_by_slug(cls,slug):
        post = cls.query.filter_by(slug=slug).first()
        return post
        
    @classmethod
    def get_all_tag_posts(cls,tagname,page):
        all_posts = []
        POSTS_PER_PAGE = 2
        tag = Tag.get_tag_by_name(tagname)
        print ("tag id associated with the tagname : {}".format(tag.id))
        all_posts = Post.query.join(assoc_table).filter (assoc_table.c.tag_id == tag.id and assoc_table.c.post_id == Post.id).order_by(Post.date.desc()).paginate(page,POSTS_PER_PAGE,False)
        print (all_posts.items)
        print (all_posts.has_prev)
        print (all_posts.has_next)
        return all_posts

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        if self.id:
            db.session.commit()
            return True
        else:
            db.session.rollback()
            return False
            
    def save_edited_to_db(self):
        db.session.flush()
        if self.id:
            db.session.commit()
            return True
        else:
            db.session.rollback()
            return False
