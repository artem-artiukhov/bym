"""
    Stage configuration
    Use env var to override
"""
import os

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'microblog')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'microblog')

SQLALCHEMY_DATABASE_URI = \
    f'postgresql://microblog:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/microblog'
