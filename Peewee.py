import os

from peewee import CharField, Model, IntegerField, DateTimeField, SqliteDatabase

# 指定database的路径为同该.py文件目录下的test.db数据库
# 而且便于后边其他脚本的导入（主要是为了db.atomic()的使用）
dbpath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'app.db'
)
# 初始化数据库
db = SqliteDatabase(dbpath)

class ArticleTypeModel(Model):
    title = CharField()
    href = CharField()
    id = CharField()

    class Meta:
        table_name = 'article_types'
        database = db


class Counter(Model):
    title = CharField()
    count = IntegerField()

    class Meta:
        table_name = 'counters'
        database = db

class ArticleModel(Model):
    title = CharField()
    href = CharField()
    authorID = CharField()
    authorName = CharField()
    # 作者链接
    authorHref = CharField()
    # 类型
    types = CharField()
    # 文章内容
    content = CharField()
    # 阅读数
    read = CharField()
    # 评价数
    comment = CharField()
    # 收藏数
    collect = CharField()
    # 是否全部信息
    isAllInfo = CharField()
    # 简介
    brief = CharField()

    class Meta:
        table_name = 'article'
        database = db
