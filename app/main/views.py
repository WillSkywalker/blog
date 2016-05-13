from datetime import datetime
from flask import render_template, session, redirect, url_for
from num2words import num2words
from sqlalchemy import desc


from . import main
from .. import db
from ..models import Article, Tag

@main.route('/')
def index():
    articles_list = Article.query.order_by(-Article.id).limit(8).all()
    articles = []
    for a in range(0, len(articles_list), 2):
        if a+1 >= len(articles_list):
            articles.append((articles_list[a], None))
        else:            
            articles.append((articles_list[a], articles_list[a+1]))
    return render_template('index.html', articles=articles)


@main.route('/<int:num>')
def article_page(num):
    article = Article.query.filter_by(id=num).first()
    if article:
        return render_template('page.html', article=article)
    else:
        return render_template('not-yet.html')


@main.route('/list')
@main.route('/list/<int:page>')
def list_page(page=1):
    pagination = Article.query.order_by(-Article.id).paginate(page, per_page=10, error_out=False)
    numname = num2words(pagination.page)
    if pagination.items:
        return render_template('list.html', pagination=pagination, numname=numname)
    else:
        return render_template('not-yet.html')


@main.route('/tag')
@main.route('/tag/<name>')
def tags(name=None):
    if name:
        tag = Tag.query.filter_by(tagname=name).first()
        if tag:
            return render_template('tags.html', tag=tag)
    taglist = Tag.query.all()
    taglist.sort(key=lambda x: x.articles.count(), reverse=True)
    return render_template('tags-list.html', tags=taglist)

