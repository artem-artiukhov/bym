"""Default configuration

Use env var to override
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(PROJECT_ROOT, *x)
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://microblog_service@localhost/microblog_service'
SQLALCHEMY_TRACK_MODIFICATIONS = False
