from datetime import datetime

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                decode_token)
from sqlalchemy import or_

from microblog.api.schemas import LoginInfoSchema
from microblog.commons.helpers import utc_date_obj_from_ts
from microblog.models import LoginInfo


class UserLoginManager:
    """User Login Info Manager."""

    @classmethod
    def create_user_login(cls, user, uli=None):
        """Create access and refresh tokens with login information."""
        # Create new pairs of access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        decoded_at = decode_token(access_token)
        decoded_rt = decode_token(refresh_token)

        if uli:
            cls.revoke(uli)

        login_info = LoginInfoSchema().load(
            {'user_agent': request.headers.get('User-Agent'),
             'ip_address': request.remote_addr,
             'expires_at': utc_date_obj_from_ts(decoded_at['exp'], format_to_str=True),
             'expires_rt': utc_date_obj_from_ts(decoded_rt['exp'], format_to_str=True),
             'jti_at': decoded_at['jti'],
             'jti_rt': decoded_rt['jti']})

        return access_token, refresh_token, login_info

    @staticmethod
    def get_login_info_by_access_jti(user, jti):
        return user.login_info.filter_by(jti_at=jti).first()

    @staticmethod
    def get_login_info_by_refresh_jti(user, jti):
        return user.login_info.filter_by(jti_rt=jti).first()

    @staticmethod
    def revoke(uli):
        uli.revoked = True
        uli.save_to_db()

    @staticmethod
    def revoke_all_tokens(user):
        for uli in user.login_info.filter_by(revoked=False).all():
            uli.revoked = True

    @staticmethod
    def add_login_info(login_info, user):
        user.login_info.append(login_info)

    @staticmethod
    def clean_expired_login_info():
        LoginInfo.query.filter(
            LoginInfo.expires_rt <= datetime.utcnow()).delete()

    @staticmethod
    def is_token_revoked(jti):
        """Check if JTI is revoked (blacklisted)."""
        res = LoginInfo.query.filter_by(revoked=True).filter(
            or_(LoginInfo.jti_at == jti, LoginInfo.jti_rt == jti)).first()
        return bool(res)
