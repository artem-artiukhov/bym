from flask import Blueprint, jsonify
from {{cookiecutter.app_name}}.extensions import db

blueprint = Blueprint('core_views', __name__)


@blueprint.route('/healthcheck')
def healthcheck():
    """ Performs a healthcheck """
    db.session.execute('SELECT 1;')
    return jsonify({'status': 'OK'})
