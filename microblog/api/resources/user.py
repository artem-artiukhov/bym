from flask import request
from .base import BaseResource
from microblog.commons.pagination import paginate

from microblog.models import User
from microblog.extensions import db
from microblog.api.schemas import UserSchema


class UserResource(BaseResource):
    """Single object resource
    """

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"data": schema.dump(user).data}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user, errors = schema.load(request.json, instance=user)
        if errors:
            return errors, 422

        return {"data": schema.dump(user).data}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "OK"}


class UserList(BaseResource):
    """Creation and get_all
    """

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(user)
        db.session.commit()

        return {"data": schema.dump(user).data}, 201
