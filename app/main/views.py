from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .. import db
from ..models import Article

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


@main.route('/list/<int:page>')
def list_page(page):
    articles_list = Article.query.order_by(-Article.id).limit(8).all()
    if article:
        return render_template('page.html', title=article.title, subtitle=article.subtitle,
                               content=article.content, tags=article.tags)
    else:
        return render_template('not-yet.html')


@main.route('/tag/<name>')
def tags(name):
    return render_template('not-yet.html')


