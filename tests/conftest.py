import inspect
import pytest

import microblog.models
from microblog.app import create_app
from microblog.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture(scope='session')
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(autouse=True)
def cleanup(db):
    """ A little hack that cleans all produced db records after each test function execution """
    yield
    for _, model in inspect.getmembers(microblog.models, inspect.isclass):
        db.session.query(model).delete()
    db.session.commit()
