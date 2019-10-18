# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
login_manager = LoginManager(app)



@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
login_manager.login_message = "请先登录！" #提示信息自动会以flash()形式输出


#模版上下文 与 return render_template搭配使用
@app.context_processor
def inject_user():
    #models没有引入app实例，所以不要紧.但是引入了watchlist里的db，所以要在db创建后才能导入
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


#为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
from watchlist import views, errors, commands

