"""Decorators Module."""
from functools import wraps

from flask import request
from flask_jwt_extended import get_raw_jwt, current_user

import microblog.commons.errors as err
from microblog.commons.exceptions import ServiceError
from microblog.managers.login import UserLoginManager


def verify_identity(jwt):
    """Compare API-call identity with existing login information:
        * user existence
        * user state (active/not active)
        * user-agent
        * ip-address
    """

    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
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

            # crunch as swagger sends redundant "user" key into kwargs
            kwargs['user'] = current_user
            kwargs['uli'] = uli

            return func(*args, **kwargs)

        return wrapper

    return inner_function
