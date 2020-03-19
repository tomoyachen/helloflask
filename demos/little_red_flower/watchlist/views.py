# -*- coding: utf-8 -*-


from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func

from watchlist import app, db
from watchlist.models import User, Movie, Message, Log
import time, datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or len(year) > 20 or len(title) > 20:
            flash('输入异常！')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('index'))

    movies = Movie.query.order_by(Movie.teacherId.asc(), Movie.year.asc(), Movie.id.asc()).all()
    if current_user.is_authenticated and current_user.isAdmin == 0:
        movies = Movie.query.filter_by(teacherId=current_user.id).order_by(Movie.teacherId.asc(), Movie.year.asc(), Movie.id.asc()).all()

    #瞎搞
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
        try:
            teacherId = request.form['teacherId']
            movie.teacherId = teacherId
        except:
            pass

        if not title or len(year) > 20 or len(title) > 20:
            flash('输入异常！')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year

        db.session.commit()
        flash('更新成功！')
        return redirect(url_for('studentinfo'))

    teacherlist = User.query.order_by(User.id.asc()).all()
    return render_template('edit.html', movie=movie, teacherlist=teacherlist)


@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def delete(movie_id):
    if request.method == 'GET':
        flash('刚才的操作失败了，建议使用浏览器使用本系统~')
        return redirect(url_for('studentinfo'))

    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('studentinfo'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

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

        user = User.query.get_or_404(current_user.id)
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
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':


        title = request.form['title']
        year = request.form['year']

        if not title or len(year) > 20 or len(title) > 20:
            flash('输入异常！')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year, flower=0)
        if current_user.isAdmin == 0:
            movie.teacherId = current_user.id
        db.session.add(movie)
        db.session.commit()
        flash('添加成功！')
        return redirect(url_for('studentinfo'))

    movies = Movie.query.order_by(Movie.teacherId.asc(), Movie.year.asc(), Movie.id.asc()).all()
    if current_user.isAdmin == 0:
        movies = Movie.query.filter_by(teacherId=current_user.id).order_by(Movie.teacherId.asc(), Movie.year.asc(), Movie.id.asc()).all()

    teacherlist = User.query.all()
    teacher_dict = {}
    for teacher in teacherlist:
        teacher_dict[teacher.id] = teacher.name
    print(teacher_dict)
    return render_template('studentinfo.html', movies=movies, teacher_dict=teacher_dict)


@app.route('/teacherinfo', methods=['GET', 'POST'])
def teacherinfo():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if current_user.isAdmin != 1:
        return redirect(url_for('index'))

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

        if not password or len(password) > 20:
            flash('密码必须小于20位')
            return redirect(url_for('settings'))

        if password != validate_password:
            flash('密码不一致')
            return redirect(url_for('settings'))

        user = User(name=name, username=username)
        user.set_password(password)
        db.session.add(user)
        count = db.session.commit()
        print("count", count)
        flash('添加成功！')

        return redirect(url_for('teacherinfo'))

    teacherlist = User.query.order_by(User.id.asc()).all()

    #瞎搞
    result = db.session.query(Movie.teacherId, func.count(Movie.teacherId).label('count'), ).group_by(Movie.teacherId).all()
    student_count_dict = {}
    for item in result:
        student_count_dict[item[0]] = item[1]
    print(student_count_dict)

    return render_template('teacherinfo.html', teacherlist=teacherlist, student_count_dict=student_count_dict)



@app.route('/movie/editTeacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def editTeacher(teacher_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if current_user.isAdmin != 1:
        return redirect(url_for('index'))

    teacher = User.query.get_or_404(teacher_id)
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

        user = teacher
        user.name = name
        user.username = username

        if len(password) > 0 and len(validate_password) > 0:
            if password == validate_password:
                user.set_password(password)
            else:
                flash('前后密码不一致！')
                return redirect(url_for('settings'))

        db.session.commit()
        flash('成功更新!')
        return redirect(url_for('teacherinfo'))

    return render_template('editTeacher.html', teacher=teacher)


@app.route('/movie/deleteTeacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def deleteTeacher(teacher_id):
    if request.method == 'GET':
        flash('刚才的操作失败了，建议使用浏览器使用本系统~')
        return redirect(url_for('teacherinfo'))

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    if current_user.isAdmin != 1:
        return redirect(url_for('index'))

    user = User.query.get_or_404(teacher_id)
    if user.isAdmin == 1:
        flash('管理员无法被删除！')
        return redirect(url_for('teacherinfo'))
    db.session.delete(user)
    db.session.commit()
    flash('删除成功！')
    return redirect(url_for('teacherinfo'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入异常！')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user == None:
            flash('用户不存在！')
            return redirect(url_for('login'))
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
    for message in messages:
        message.timestamp = message.timestamp + datetime.timedelta(hours=8)
    return render_template('message.html', messages=messages)


@app.route('/movie/deleteMessage/<int:message_id>', methods=['GET', 'POST'])
@login_required
def deleteMessage(message_id):
    if request.method == 'GET':
        flash('刚才的操作失败了，建议使用浏览器使用本系统~')
        return redirect(url_for('message'))

    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('留言已删除')
    return redirect(url_for('message'))

@app.route('/student/addFlower/<int:student_id>', methods=['GET', 'POST'])
@login_required
def addFlower(student_id):
    if request.method == 'GET':
        flash('刚才的操作失败了，建议使用浏览器使用本系统~')
        return redirect(url_for('index'))

    movie = Movie.query.get_or_404(student_id)
    # time.sleep(1)
    update_count = Movie.query.filter_by(id=movie.id).filter_by(version=movie.version).update({'flower': movie.flower + 1, 'version': movie.version + 1 })
    if update_count == 0:
        flash('您点的太快啦！系统反应不过来了~')
        return redirect(url_for('index'))

    flash('恭喜%s小朋友，获得一枚小星星~' %movie.title)
    print(movie.title, movie.flower)
    writeLog(1, student_id)
    time.sleep(1)
    return redirect(url_for('index'))

@app.route('/student/removeFlower/<int:student_id>', methods=['GET', 'POST'])
@login_required
def removeFlower(student_id):
    if request.method == 'GET':
        flash('刚才的操作失败了，建议使用浏览器使用本系统~')
        return redirect(url_for('index'))

    movie = Movie.query.get_or_404(student_id)
    # time.sleep(1)
    if movie.flower == 0:
        flash('小朋友的分数不够扣了~')
        return redirect(url_for('index'))
    update_count = Movie.query.filter_by(id=movie.id).filter_by(version=movie.version).update({'flower': movie.flower - 1, 'version': movie.version + 1 })
    if update_count == 0:
        flash('您点的太快啦！系统反应不过来了~')
        return redirect(url_for('index'))

    flash('%s小朋友，很遗憾失去一枚小星星~' %movie.title)
    print(movie.title, movie.flower)
    writeLog(2, student_id)
    return redirect(url_for('index'))

@app.route('/log', methods=['GET'])
def log():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    logs_dict = {}
    for log in logs:
        movie = Movie.query.filter_by(id=log.studentId).first()
        log.teacherId = movie.teacherId
        if current_user.is_authenticated and current_user.isAdmin == 0:
            if log.teacherId != current_user.id:
                continue
        log.timestamp = log.timestamp + datetime.timedelta(hours=8)
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