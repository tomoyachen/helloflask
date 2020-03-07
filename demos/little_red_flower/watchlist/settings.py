import os
import sys

from watchlist import app

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev') #使用flash需要session，使用session需要密钥
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#去除多余空行
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True