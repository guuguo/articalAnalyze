import requests
from bs4 import BeautifulSoup


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


class JuejinArticleProvider(object):
    host = "https://juejin.cn/"

    def __getNum__(self, num: int):
        return int(float(num.strip('w')) * 10000 if num[-1] == 'w' else float(
            num))

    def get_types(self):
        掘金首页 = requests.get(JuejinArticleProvider.host).text
        soup = BeautifulSoup(掘金首页)
        navList = soup.find("div", {"class": "nav-list left"}).findAll('a')
        types = []
        for a in navList:
            atype = ArticleType()
            atype.id = a.find("div").get('st:state', '')
            if len(atype.id) == 0:
                continue
            atype.href = "https://juejin.cn" + a["href"]
            atype.title = a.find("div").text.strip()
            atype.id = a.find("div").get('st:state', '')
            types.append(atype)
        return types

    def get_hotest_list(self, type: ArticleType):
        热门列表 = requests.get(type.href + "?sort=monthly_hottest").text
        soup = BeautifulSoup(热门列表)
        articleList = soup.find("ul", {"class": "entry-list"}).findAll('div', {"class": "content-box"})
        articles = []
        for content in articleList:
            artical = Article()
            titleRowA = content.find('div', {'class': 'class-row'}).find('a')
            artical.href = JuejinArticleProvider.host + titleRowA["href"]
            artical.title = titleRowA["title"]
            artical.brief = content.find('div', {'class': 'abstract'}).find('a').text.strip()

            action_area = content.find('ul', {'class': 'action-list jh-timeline-action-area'})
            artical.read = self.__getNum__(action_area.find('li', {'class': 'item view'}).find('span').text)
            artical.comment = self.__getNum__(action_area.find('li', {'class': 'item like'}).find('span').text)
            artical.like = self.__getNum__(action_area.find('li', {'class': 'item comment'}).find('span').text)

            articles.append(artical)
        return articles


provider = JuejinArticleProvider()
types = provider.get_types()
for a in types:
    print(a)
