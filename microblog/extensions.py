"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
