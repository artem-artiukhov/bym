from microblog.extensions import ma, db
from microblog.models import HashTags


class HashtagSchemaGeneric(ma.ModelSchema):
    class Meta:
        model = HashTags
        sqla_session = db.session


class HashtagCreateSchema(HashtagSchemaGeneric):
    hashtag = ma.Str(required=False)
    id = ma.Int(required=False)


class HashtagListSchema(HashtagSchemaGeneric):
    contents = ma.Nested('ContentInfoSchema', many=True, exclude=['hashtags'])

    class Meta:
        model = HashTags
        sqla_session = db.session


class HashtagInfoSchema(HashtagSchemaGeneric):

    class Meta:
        model = HashTags
        sqla_session = db.session
        exclude = ('id', 'description', 'contents')
