from sqlalchemy.exc import IntegrityError

from microblog.extensions import db, pwd_context
from .login_info import LoginInfo


class User(db.Model):
    """Basic user model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    attempts = db.Column(db.Integer, nullable=False, server_default=db.text('0'))
    blocked_until = db.Column(db.DateTime, nullable=True)

    # Relations
    login_info = db.relationship(LoginInfo, lazy='dynamic', cascade='all, delete-orphan', backref='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = pwd_context.hash(self.password)

    def __repr__(self):
        return "<User %s>" % self.username

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @staticmethod
    def verify_hash(password, _hash):
        return pwd_context.verify(password, _hash)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def generate_fake(count=100):
        """
        Static method to create pool of records in User table in order to work with it
        """
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     password='Pa$$w0rd',
                     active=True)

            db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
