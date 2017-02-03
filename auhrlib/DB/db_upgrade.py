#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    【数据库管理套件：数据库升级】
    在没有对数据库做任何更改的情况下，提升一档数据库版本。代码固定，不必深究。
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))