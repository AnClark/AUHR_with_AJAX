
"""
    【站点应用配置文件】
    在这里指定站点所需的各种必要的参数。本文件会作为对象，被应用程序的__init__模块加载。
"""

from os import path

#   【表单配置】
#   【警告！】 跨站点请求伪造保护功能（CSRF）是强制要求！
CSRF_ENABLED = True             # 跨站点请求伪造保护开关
SECRET_KEY = 'the-blue-lotus'       # CSRF 所需的密钥

#   【数据库配置】

#   指定数据库文件名
database_name = 'AUHRSystem.db'

#   获取并保存基准路径（即整个工程的根目录），以供SQLAlchemy使用
root_dir = path.abspath(path.dirname(__file__))
db_basedir = path.join(root_dir, 'db')

#   指定数据库的一些路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(db_basedir, database_name)   # 数据库路径，以统一资源标识符的形式表示
SQLALCHEMY_MIGRATE_REPO = path.join(db_basedir, 'db_repository')        # 数据迁移仓库位置。每一次对数据库做的更改都会在其中留下存档
#   =========================================================
