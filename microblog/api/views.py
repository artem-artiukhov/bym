from flask import Blueprint
from flask_restplus import Api

from microblog.api.resources import UserResource, UserList, UserSignIn, UserSignOut


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

# user auth
api.add_resource(UserSignIn, '/signin')
api.add_resource(UserSignOut, '/signout')