import logging

from flask_restplus import Resource


class BaseResource(Resource):
    """Base Resource with initialized logging."""
    pass
    # def __init__(self):
    #     super().__init__()
    #     self._log = logging.getLogger(self.__class__.__name__)
