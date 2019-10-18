import os

from dotenv import load_dotenv

#不使用Flask内置服务器时，需要手动加载环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
from watchlist import app

if __name__ == "__main__":
    app.run()