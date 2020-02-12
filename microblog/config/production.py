"""
    Production configuration
    Use env var to override
"""
import os

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

SQLALCHEMY_DATABASE_URI = \
    f'postgresql://microblog_service:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/microblog_service'  # noqa E501
