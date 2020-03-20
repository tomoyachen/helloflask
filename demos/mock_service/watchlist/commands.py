# -*- coding: utf-8 -*-
import click

from watchlist import app, db
from watchlist.models import User, Api


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    user = User(name="管理员", username="admin")
    user.set_password("Aa111111")
    user.isAdmin = 1
    db.session.add(user)

    user2 = User(name="张三", username="zhangsan")
    user2.set_password("Aa111111")
    db.session.add(user2)

    #初始学生数据
    api_list = [
        {'name': 'index', 'path': '/', 'response': "index"},
        {'name': 'aaa', 'path': '/aaa', 'response': "aaa"},

    ]


    for api in api_list:
        movie = Api(name=api['name'], path=api['path'],  response=api['response'])
        db.session.add(movie)

    db.session.commit()

    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name=username)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
