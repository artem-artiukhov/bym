"""Default configuration

Use env var to override
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(PROJECT_ROOT, *x)  # noqa E731
DEBUG = True
PROPAGATE_EXCEPTIONS = True

SECRET_KEY = '23r2@$@!DQW%#@QDasdsa2142--a(*!'

JWT_SECRET_KEY = '3434r34r3@#%4r34'
JWT_ACCESS_TOKEN_EXPIRES = 3600 * 6
JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 30
JWT_BLACKLIST_ENABLED = True

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'  # noqa E501
SQLALCHEMY_TRACK_MODIFICATIONS = False
