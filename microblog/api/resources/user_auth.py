"""User Authentication Resources Module."""
import datetime

from flask import request
from flask_jwt_extended import jwt_refresh_token_required
from flask_restplus import reqparse

import microblog.commons.errors as err
from flask_jwt_extended import get_raw_jwt, current_user
from microblog.commons.exceptions import ServiceError
from microblog.commons.helpers import (unwrap_envelope, wrap_envelope)
from microblog.extensions import jwt
from microblog.managers.login import UserLoginManager
from microblog.models import User

from .base import BaseResource

reset_pw_parser = reqparse.RequestParser()
reset_pw_parser.add_argument('token')


class UserSignIn(BaseResource):
    def post(self):
        """Sign in user by creating new pairs of refresh and access tokens."""
        if not request.is_json:
            raise ServiceError(*err.MISSING_JSON)

        data = unwrap_envelope(request.get_json())
        email = data.get('email')
        user = User.find_by_email(email)

        if not user:
            # self._log.warning('Failed to sign in - user <%s> does not exist', email)
            raise ServiceError(*err.WRONG_CREDENTIALS)

        if user.blocked_until and user.blocked_until > datetime.datetime.now():
            raise ServiceError(*err.WRONG_CREDENTIALS)

        if not User.verify_hash(data.get('password'), user.password):
            user.attempts += 1
            if user.attempts >= 5:
                user.blocked_until = datetime.datetime.now() + datetime.timedelta(minutes=5)
                user.attempts = 0
            # self._log.warning('Failed to sign in - wrong credentials for %s', user)

            user.save_to_db()

            raise ServiceError(*err.WRONG_CREDENTIALS)

        user.attempts = 0
        user.blocked_until = None

        access_token, refresh_token, uli = UserLoginManager.create_user_login(user)
        # if errors:
            # self._log.error('Failed to create user login for %s: %s', user, errors)
            # raise ServiceError(*err.MARSHMALLOW_VALIDATION_ERROR)

        UserLoginManager.add_login_info(uli, user)
        user.save_to_db()
        # self._log.debug('Created user login for %s - at: %s, rt: %s, uli: %s',
        #                 user, access_token, refresh_token, uli)
        # self._log.info('%s successfully signed in', user)

        return wrap_envelope({'msg': f'Signed in as {user.email}',
                              'access_token': access_token,
                              'refresh_token': refresh_token})


class UserSignOut(BaseResource):
    @jwt_refresh_token_required
    def post(self):
        """Sign out user by revoking all known user's tokens."""
        if not current_user or not current_user.active:
            raise ServiceError(*err.ACCESS_DENIED)

        # Get User Login Information (uli)
        token_type = get_raw_jwt()['type']
        jti = get_raw_jwt()['jti']
        uli = getattr(
            UserLoginManager,
            f'get_login_info_by_{token_type}_jti')(current_user, jti)

        if not uli:
            raise ServiceError(*err.ACCESS_DENIED)

        if request.headers.get('User-Agent') != uli.user_agent:
            UserLoginManager.revoke(uli)
            raise ServiceError(*err.ACCESS_DENIED)

        user = current_user
        uli = uli

        UserLoginManager.revoke_all_tokens(user)
        user.save_to_db()
        return wrap_envelope({'msg': 'OK'}), 200


@jwt.user_loader_callback_loader
def load_user(identity):
    return User.find_by_id(identity)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Check if request token is blacklisted (revoked)."""
    return UserLoginManager.is_token_revoked(decrypted_token['jti'])


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token['type']
    return wrap_envelope({'msg': f'The {token_type} token has expired'}), 401
