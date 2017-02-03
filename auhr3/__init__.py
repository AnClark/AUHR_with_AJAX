"""
=================== 应用主入口模块 ====================
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy     # 引入数据库模块
from flask_login import LoginManager    # 引入登录管理模块

from config import db_basedir  # 引入基准目录变量，用于SQLAlchemy与OpenID


app = Flask(__name__)

app.config.from_object('config')

# 数据库：创建数据库对象
db = SQLAlchemy(app)

# 登录管理模块：创建初始化有关对象
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


if __name__ == "__main__":
    app.run(debug=True)
