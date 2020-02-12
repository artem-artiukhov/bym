"""Decorators Module."""
import time
from functools import wraps

from flask import request
from flask_jwt_extended import get_raw_jwt, current_user
from flask_socketio import ConnectionRefusedError, disconnect

import mh_admin.commons.errors as err
from mh_admin.commons.exceptions import ServiceError, WebSocketAuthError
from mh_admin.managers.auth import WebSocketAuthManager
from mh_admin.managers.login import UserLoginManager

auth_manager = WebSocketAuthManager()


def auth_notifications(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        try:
            user = auth_manager.validate_token(token)
        except WebSocketAuthError:
            disconnect()
            raise ConnectionRefusedError
        return func(*args, user, **kwargs)

    return decorated_function


def pass_perm(roles=()):
    """Skip permission check for defined user roles."""

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            cls, user, content = args
            if not content:
                raise ServiceError(*err.ACCESS_DENIED)
            if user.role_id in roles:
                return
            return func(*args, **kwargs)

        return decorated_function

    return decorator


def verify_identity(roles=()):
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

            if roles and current_user.role_id not in roles:
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


def retry(exceptions, tries=4, delay=3, backoff=2, silent=False, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exceptions: the exception(s) to check. may be a tuple of
        exceptions to check.
    :type exceptions: Exception type, exception instance, or tuple containing
        any number of both (eg. IOError, IOError(errno.ECOMM), (IOError,), or
        (ValueError, IOError(errno.ECOMM))
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param silent: If set then no logging will be attempted
    :type silent: bool
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    try:
        len(exceptions)
    except TypeError:
        exceptions = (exceptions,)
    all_exception_types = tuple(
        set(x if type(x) == type else x.__class__ for x in exceptions))
    exception_types = tuple(x for x in exceptions if type(x) == type)
    exception_instances = tuple(x for x in exceptions if type(x) != type)

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except all_exception_types as e:
                    if (not any(x for x in exception_types if isinstance(e, x))
                            and not any(x for x in exception_instances if
                                        type(x) == type(
                                            e) and x.args == e.args)):
                        raise
                    msg = "%s, Retrying in %d seconds..." % (
                        str(e) if str(e) != "" else repr(e), mdelay)
                    if not silent:
                        if logger:
                            logger.warning(msg)
                        else:
                            print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
