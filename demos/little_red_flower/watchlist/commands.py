# -*- coding: utf-8 -*-
import click

from watchlist import app, db
from watchlist.models import User, Movie, Message


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

    user2 = User(name="老师", username="teacher")
    user2.set_password("Aa111111")
    db.session.add(user2)

    #初始学生数据
    movies = [
        {'title': '萨达', 'year': '', 'flower': 0},
        {'title': '是的撒', 'year': '', 'flower': 0},
        {'title': '灌砂法', 'year': '', 'flower': 0},
        {'title': '实打实熙', 'year': '', 'flower': 0},
        {'title': '大', 'year': '', 'flower': 0},
        {'title': '阿斯达', 'year': '', 'flower': 0},
        {'title': '撒打发', 'year': '', 'flower': 0},
        {'title': '序章', 'year': '', 'flower': 0},
        {'title': '萨达啊', 'year': '', 'flower': 0},
        {'title': '序章', 'year': '', 'flower': 0},
        {'title': '阿萨德', 'year': '', 'flower': 0},
        {'title': '啊', 'year': '', 'flower': 0},
    ]

    movies = [
        {'title': '徐千寻', 'year': '', 'flower': 0},
        {'title': '周君灏', 'year': '', 'flower': 0},
        {'title': '万子坤', 'year': '', 'flower': 0},
        {'title': '聂峻熙', 'year': '', 'flower': 0},
        {'title': '龙雨薇', 'year': '', 'flower': 0},
        {'title': '周诗琪', 'year': '', 'flower': 0},
        {'title': '周胤辰', 'year': '', 'flower': 0},
        {'title': '胡彭飞', 'year': '', 'flower': 0},
        {'title': '魏文哲', 'year': '', 'flower': 0},
        {'title': '胡奕成', 'year': '', 'flower': 0},
        {'title': '李煊赫', 'year': '', 'flower': 0},
        {'title': '马钰婷', 'year': '', 'flower': 0},
    ]


    for m in movies:
        movie = Movie(title=m['title'], year=m['year'],  flower=m['flower'])
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
        user = User(username=username, name='老师')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
