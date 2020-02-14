from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from microblog import api, commands, views
from microblog.commons.exceptions import ServiceError
from microblog.extensions import (db, migrate, jwt)


def create_app(config=None, testing=False):
    """Application factory, used to create application
    """
    app = Flask('microblog')

    configure_app(app, testing)
    configure_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shellcontext(app)
    register_flask_handlers(app)

    return app

def register_flask_handlers(app):

    @app.errorhandler(ServiceError)
    def handle_service_error(error):
        """Register and handle ServiceError."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle general exceptions."""
        if isinstance(error, HTTPException):
            return error
        return 'Internal Server Error', 500


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('microblog.config')

    if testing is True:
        # override with testing config
        app.config.from_object('microblog.config.test')
    # override with env variable, fail silently if not set
    app.config.from_envvar("APPLICATION_CONFIG", silent=True)
    app.url_map.strict_slashes = False


def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(views.blueprint)


def register_commands(app):
    """ Register custom commands """
    app.cli.add_command(commands.createsuperuser)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db}
    app.shell_context_processor(shell_context)
