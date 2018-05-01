from project import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    @classmethod
    def get_all_tags(cls):
        existing_tags = []
        tags = cls.query.all()
        for tag in tags:
            t = (str(tag.id),str(tag.name))
            existing_tags.append(t)
        return existing_tags

    @classmethod
    def get_tag_by_id(cls,id):
        tag = cls.query.filter_by(id=id).first()
        return tag
        
    @classmethod
    def get_tag_by_name(cls,name):
        tag = cls.query.filter_by(name=name).first()
        return tag
        
        
assoc_table = db.Table('posts_tags',
         db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
         db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
         )
        





