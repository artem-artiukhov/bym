import click
from flask.cli import with_appcontext
from microblog.extensions import db


@click.command()
@with_appcontext
def createsuperuser():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from microblog.models import User

    click.echo("creating user")
    user = User(
        username='admin',
        email='admin@mail.com',
        password='admin',
        active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
