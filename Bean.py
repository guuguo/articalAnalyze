
class ArticleType(object):
    """文章类型类"""

    def __init__(self):
        self.title = ''
        self.href = ''
        self.id = ''

    def __str__(self):
        return 'href：' + self.href + "\n" + 'title：' + self.title + "\n" + 'id：' + self.id


class Article(object):
    """文章类"""

    def __init__(self):
        self.title = ''
        self.href = ''
        self.authorID = ''
        self.authorName = ''
        # 作者链接
        self.authorHref = ''
        # 类型
        self.types = ''
        # 文章内容
        self.content = ''
        # 阅读数
        self.read = ''
        # 评价数
        self.comment = ''
        # 收藏数
        self.collect = ''
        # 是否全部信息
        self.isAllInfo = ''
        # 简介
        self.brief = ''

    def __str__(self):
        return 'href：' + self.href + "\n" + 'title：' + self.title
