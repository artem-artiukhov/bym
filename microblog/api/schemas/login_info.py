import ipaddress

from marshmallow import validates, ValidationError

from microblog.extensions import ma, db
from microblog.models import LoginInfo


class LoginInfoSchema(ma.ModelSchema):
    """
        Login Info Schema.
    """
    @validates
    def valdiate_ipv4(self, data):
        try:
            ipaddress.ip_address(data)
        except ValueError:
            raise ValidationError(f'Invalid IP-address {data}')

    user_agent = ma.String(required=True)
    ip_address = ma.String(required=True)
    expires_at = ma.DateTime(required=True)
    expires_rt = ma.DateTime(required=True)
    jti_at = ma.String(required=True)
    jti_rt = ma.String(required=True)

    class Meta:
        model = LoginInfo
        sqla_session = db.session
        dump_only = ('id', 'user_id', 'expires')
