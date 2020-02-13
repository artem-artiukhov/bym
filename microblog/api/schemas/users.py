from microblog.extensions import ma, db
from microblog.models import User


class UserSchema(ma.ModelSchema):

    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session
        exclude = ('login_info',)
