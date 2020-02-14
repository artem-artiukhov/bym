from flask import request
from flask_jwt_extended import jwt_required

import microblog.commons.errors as err
from microblog.api.schemas import PostInfoSchema, PostCreateSchema
from microblog.commons.exceptions import ServiceError
from microblog.commons.helpers import wrap_envelope, unwrap_envelope
from microblog.commons.decorators import get_user_uli
from microblog.commons.pagination import paginate
from microblog.extensions import db
from microblog.models import Post
from .base import BaseResource


class Posts(BaseResource):
    """Content management resource."""

    @jwt_required
    def get(self):
        query = Post.get_view_query()
        return paginate(query, PostInfoSchema(many=True))

    @jwt_required
    def post(self):
        if not request.is_json:
            raise ServiceError(*err.MISSING_JSON)

        user, uli = get_user_uli()

        data = request.get_json()
        data['data']['author_id'] = user.id
        print(data)

        content_new = PostCreateSchema().load(unwrap_envelope(data))

        content_new.save_to_db()
        return PostInfoSchema().dump(content_new), 201

    @jwt_required
    def delete(self):
        if not request.is_json:
            raise ServiceError(*err.MISSING_JSON)

        user, uli = get_user_uli()

        content_id = request.get_json().get('data', {}).get('id')
        cont_to_del = Post.find_by_id(content_id)

        if not cont_to_del:
            self._log.error('Failed to delete content id %s by %s: '
                            'No such content', content_id, user)
            raise ServiceError(*err.CONTENT_NOT_FOUND)

        if cont_to_del.author_id != user.id:
            raise ServiceError(*err.ACCESS_DENIED)


        db.session.delete(cont_to_del)
        db.session.commit()

        return wrap_envelope({'msg': f'Content id {cont_to_del.id} deleted'})


class MyPosts(BaseResource):
    @jwt_required
    def get(self):
        if not request.is_json:
            raise ServiceError(*err.MISSING_JSON)

        user, uli = get_user_uli()

        query = Post.query.filter_by(author_id=user.id)

        return paginate(query, PostInfoSchema(many=True))


class PostView(BaseResource):
    """Endpoint to review certain content using its id value."""
    @jwt_required
    def get(self, p_id):
        cont_to_show = Post.find_by_id(p_id)
        if not cont_to_show:
            raise ServiceError(*err.CONTENT_NOT_FOUND)

        user, uli = get_user_uli()

        if cont_to_show.author_id != user.id:
            raise ServiceError(*err.ACCESS_DENIED)

        return PostInfoSchema().dump(cont_to_show)
