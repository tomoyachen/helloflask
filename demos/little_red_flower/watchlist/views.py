# -*- coding: utf-8 -*-


from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func

from watchlist import app, db
from watchlist.models import User, Movie, Message, Log
import time


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or len(year) > 60 or len(title) > 60:
            flash('输入异常！')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('index'))

    movies = Movie.query.order_by(Movie.year.asc(), Movie.id.asc()).all()

    #瞎搞
    import datetime
    _start_time = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
    _end_time = datetime.datetime.now().strftime("%Y-%m-%d") + " 23:59:59"
    result = db.session.query( Log.studentId, func.sum(Log.amount).label('count'), ).filter(Log.timestamp >= _start_time).filter(Log.timestamp <= _end_time).group_by(Log.studentId).all()
    # result = db.session.query( Log.studentId, func.count(1).label('count'), ).filter(db.cast(Log.timestamp, db.DATE) == db.cast(datetime.datetime.now(), db.DATE)).group_by(Log.studentId).all()
    today_star_dict = {}
    for item in result:
        today_star_dict[item[0]] = item[1]
    print(today_star_dict)


    return render_template('index.html', movies=movies, today_star_dict=today_star_dict)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or len(year) > 60 or len(title) > 60:
            flash('输入异常！')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('更新成功！')
        return redirect(url_for('studentinfo'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('studentinfo'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        validate_password = request.form['validate_password']

        if not name or len(name) > 20:
            flash('姓名必须小于20位')
            return redirect(url_for('settings'))

        if not username or len(username) > 20:
            flash('用户名必须小于20位')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        user.username = username

        if len(password) >0 and len(validate_password) > 0:
            if password == validate_password:
                user.set_password(password)
                logout()
            else:
                flash('前后密码不一致！')
                return redirect(url_for('settings'))

        db.session.commit()
        flash('成功更新!')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.route('/studentinfo', methods=['GET', 'POST'])
def studentinfo():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or len(year) > 60 or len(title) > 60:
            flash('输入异常！')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year, flower=0)
        db.session.add(movie)
        db.session.commit()
        flash('添加成功！')
        return redirect(url_for('studentinfo'))

    movies = Movie.query.order_by(Movie.year.asc(), Movie.id.asc()).all()
    return render_template('studentinfo.html', movies=movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入异常！')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('index'))

        flash('错误的用户名或密码！')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功！')
    return redirect(url_for('index'))




@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        name = request.form['messagename']
        body = request.form['messagebody']

        if not name or not body:
            flash('输入异常！')
            return redirect(url_for('message'))

        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('留言成功！')
        return redirect(url_for('message'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('message.html', messages=messages)


@app.route('/movie/deleteMessage/<int:message_id>', methods=['POST'])
@login_required
def deleteMessage(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('留言已删除')
    return redirect(url_for('message'))

@app.route('/student/addFlower/<int:student_id>', methods=['POST'])
@login_required
def addFlower(student_id):
    movie = Movie.query.get_or_404(student_id)
    movie.flower += 1;
    db.session.commit()
    flash('恭喜%s小朋友，获得一枚小星星~' %movie.title)
    print(movie.title, movie.flower)
    writeLog(1, student_id)
    time.sleep(1)
    return redirect(url_for('index'))

@app.route('/student/removeFlower/<int:student_id>', methods=['POST'])
@login_required
def removeFlower(student_id):
    movie = Movie.query.get_or_404(student_id)
    movie.flower -= 1;
    db.session.commit()
    flash('%s小朋友，很遗憾失去一枚小星星~' %movie.title)
    print(movie.title, movie.flower)
    writeLog(2, student_id)
    return redirect(url_for('index'))

@app.route('/log', methods=['GET'])
def log():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    logs_dict = {}
    for log in logs:
        date = log.timestamp.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        if date in logs_dict.keys():
            logs_dict[date].append(log)
        else:
            logs_dict[date] = []
            logs_dict[date].append(log)
    print(logs_dict)
    return render_template('log.html', logs=logs, logs_dict=logs_dict)


def writeLog(type, studentId):
    amount = 0
    if type == 1:
        amount = 1
    elif type ==2:
        amount = -1
    student = Movie.query.get_or_404(studentId)
    studentName = student.title
    studentBalance = student.flower

    log = Log(type=type, amount=amount, studentBalance=studentBalance, studentId=studentId, studentName=studentName)
    db.session.add(log)
    db.session.commit()