import json
from functools import reduce

import requests
from bs4 import BeautifulSoup

from Bean import ArticleType, Article
from Peewee import ArticleTypeModel, ArticleModel, Counter


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

    cursor = ""

    def get_hotest_list(self, type: ArticleType):
        data = {
            "id_type": 2,
            "sort_type": 0,
            "cate_id": type.id,
            "cursor": JuejinArticleProvider.cursor,
            "limit": 20
        }
        热门列表 = requests.post("https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed",
                             json=data).text
        json_data = json.loads(热门列表)
        JuejinArticleProvider.cursor = json_data['cursor']

        articles = []
        for content in json_data['data']:
            article_info = content['article_info']
            artical = Article()
            artical.id = article_info["article_id"]
            artical.href = JuejinArticleProvider.host + "/post/" + article_info["article_id"]
            artical.title = article_info["title"]
            artical.brief = article_info["brief_content"]
            artical.view = article_info["view_count"]
            artical.comment = article_info["comment_count"]
            artical.collect = article_info["collect_count"]
            artical.like = article_info["digg_count"]
            # author
            author_info = content['author_user_info']
            artical.authorName = author_info["user_name"]
            artical.authorID = author_info["user_id"]
            artical.authorHref = JuejinArticleProvider.host + "/user/" + author_info["user_id"]
            artical.authorAvatar = author_info["avatar_large"]

            artical.tags = reduce(lambda x, y: x + "-" + y, content["tags"], "")

            articles.append(artical)
        return articles


def checkArticleTypes(provider: JuejinArticleProvider):
    if not ArticleTypeModel.table_exists():
        ArticleTypeModel.create_table()

    if ArticleTypeModel.select().count() > 0:
        types = provider.get_types()
        for a in types:
            p = ArticleTypeModel.create(title=a.title, href=a.href, id=a.id)
            p.save()


def checkArticles(provider: JuejinArticleProvider):
    if not ArticleModel.table_exists():
        ArticleModel.create_table()
    types = ArticleTypeModel.select().execute()

    for a in types:
        JuejinArticleProvider.cursor = ""
        counter = Counter.get_or_none(Counter.title == a.title)
        if counter is None:
            type_count = 0
        else:
            type_count = counter.count()
        while type_count < 10:
            articles = provider.get_hotest_list(a, )
            for a in types:
                p = ArticleModel.create(title=a.title, href=a.href, id=a.id)
                p.save()


def checkCounter():
    if not Counter.table_exists():
        Counter.create_table()


provider = JuejinArticleProvider()

checkCounter()
checkArticleTypes(provider)
checkArticles(provider)
