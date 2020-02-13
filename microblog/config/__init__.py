"""Default configuration

Use env var to override
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(PROJECT_ROOT, *x)
DEBUG = False
PROPAGATE_EXCEPTIONS = False

SECRET_KEY = '23r2@$@!DQW%#@QDasdsa2142--a(*!'

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'  # noqa E501
SQLALCHEMY_TRACK_MODIFICATIONS = False
