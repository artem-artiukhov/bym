"""Exceptions Module."""

from microblog.commons.helpers import wrap_envelope


class ServiceError(Exception):
    """Error class intended to return flask response with error code."""

    def __init__(self, message, error_code, status_code=400, return_msg=False):
        """Constructor class."""
        super().__init__()
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.return_msg = return_msg

    def to_dict(self):
        """Return data placed inside dictionary."""
        response = {'error_code': self.error_code}
        if self.return_msg:
            response['msg'] = self.message
        return wrap_envelope(response)
