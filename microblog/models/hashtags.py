from microblog.extensions import db


class AssociationHashTags(db.Model):
    __tablename__ = 'association_hash_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)


class HashTags(db.Model):
    """
    Helper table to store data about tags (keywords) on content.
    """
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String)
    description = db.Column(db.String)
