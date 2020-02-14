from datetime import datetime

from sqlalchemy.exc import IntegrityError

import microblog.commons.errors as err
from microblog.commons.exceptions import ServiceError
from microblog.extensions import db
from microblog.models.hashtags import AssociationHashTags


class Post(db.Model):
    """
    Content model
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    title = db.Column(db.String, nullable=False, server_default="Not provided yet")
    body = db.Column(db.String, server_default="Not provided yet")
    raw = db.Column(db.String, server_default="Not provided yet")

    # One to Many or Many to One Relations
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    author = db.relationship('User', backref='content', foreign_keys=[author_id])

    # Many to many relations using association tables
    hashtags = db.relationship('HashTags', secondary=AssociationHashTags.__table__, lazy='dynamic', backref='contents')

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ServiceError(*err.DATABASE_ERROR)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
