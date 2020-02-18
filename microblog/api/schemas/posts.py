from marshmallow import pre_load

from microblog.extensions import ma, db
from microblog.commons.mixins import DataSchemaMixin
from microblog.commons.helpers import unwrap_envelope, wrap_envelope
from microblog.models import Post, HashTags
from microblog.api.schemas.hashtags import (HashtagInfoSchema,
                                            HashtagCreateSchema)
from microblog.api.schemas import UserSchema


class PostSchemaGeneric(DataSchemaMixin, ma.ModelSchema):

    class Meta:
        model = Post
        sqla_session = db.session

    @pre_load
    def check_hashtags(self, data, **kwargs):
        """Replace hashtags wording with proper ids in case if they already exists."""
        data_ = unwrap_envelope(data)
        hashtags = data_.get('hashtags')

        if not hashtags:
            return data

        ht_new = []
        for hashtag in hashtags:
            ht = HashTags.query.filter_by(hashtag=hashtag['hashtag']).first()
            ht_new.append({'id': ht.id} if ht else hashtag)

        data_['hashtags'] = ht_new

        return wrap_envelope(data_)


class PostInfoSchema(PostSchemaGeneric):
    hashtags = ma.Nested(HashtagInfoSchema, many=True)
    author = ma.Nested(UserSchema(only=('email', 'active', 'id')))


class PostCreateSchema(PostSchemaGeneric):
    author_id = ma.Integer(required=True)
    hashtags = ma.Nested(HashtagCreateSchema, many=True)
