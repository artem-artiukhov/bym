"""Errors module."""

# Errors: <message> <error_code> <server_response_code>
GENERAL_ERROR_CODE = ('General error', 1000, 400)
WRONG_CREDENTIALS = ('Wrong credentials', 1001, 401)
USER_DOES_NOT_EXIST = ('User does not exist', 1002, 404)
MISSING_JSON = ('Missing JSON in request', 1003, 400)
MARSHMALLOW_VALIDATION_ERROR = ('Failed to validate payload fields', 1004, 400)
BROKEN_TOKEN = ('You have provided broken token!', 1005, 400)
CONFIRMED_ACCOUNT = ('Your account has already been confirmed. Thanks!', 1006, 400)
INVALID_TOKEN = ('The confirmation link is invalid.', 1007, 400)
EXPIRED_TOKEN = ('Sorry, your link has expired. Please address to administrator'
                 ' in order to receive new confirmation  link.', 1008, 400)
ACCESS_DENIED = ('Access denied', 1009, 403)
PASSWORDS_DO_NOT_MATCH = ('Passwords do not match', 1010, 403)
WRONG_CURRENT_PASSWORD = ('Wrong current password', 1011, 403)
DUPLICATE_RECORD = ('This user already exists!', 1012, 400)
NOT_ALLOWED = ('You are not allowed for this action!', 1013, 403)
S3_STORAGE_ERROR = ('Storage service is not available', 1014, 503)
DATABASE_ERROR = ('Content can not be added due to data inconsistency.', 1015, 400)
MEDIA_TYPE_NOT_ALLOWED = ('This media type cannot be uploaded', 1016, 403)
CONTENT_NOT_FOUND = ('Requested content was not found', 1017, 404)
