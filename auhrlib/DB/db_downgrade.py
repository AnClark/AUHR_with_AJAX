#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    【数据库管理套件：数据库降级】
    用于撤回对数据库所做的更改，将数据库还原至更改前的上个状态。代码固定，不必深究。
"""


from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))