from microblog.extensions import db


class LoginInfo(db.Model):
    """User Login Info Model."""

    __tablename__ = 'login_info'

    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    expires_rt = db.Column(db.DateTime, nullable=False)

    # Access and Refresh Token JTIs
    jti_at = db.Column(db.String(120), unique=True, nullable=False)
    jti_rt = db.Column(db.String(120), unique=True, nullable=False)
    revoked = db.Column(db.Boolean, default=False, nullable=False)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_itself(self):
        db.session.delete(self)
        db.session.commit()


db.Index('idx_jti_at', LoginInfo.jti_at)
db.Index('idx_jti_rt', LoginInfo.jti_rt)
db.Index('idx_expires_rt', LoginInfo.expires_rt)
