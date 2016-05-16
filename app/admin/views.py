from flask import render_template, session, redirect, url_for, current_app
from . import admin, forms
from ..models import Article, Tag
from .. import db
from os import environ
from datetime import datetime
from markdown import markdown
import bleach


ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'img',
                'h1', 'h2', 'h3', 'p']

ALLOWED_ATTRS = {'*': ['class'],
                 'a': ['href', 'rel'],
                 'img': ['src', 'alt']}


def markdown_to_html(value):
    return bleach.linkify(bleach.clean(markdown(value, output_format='html'), 
                                tags=ALLOWED_TAGS, strip=True, attributes=ALLOWED_ATTRS))


@admin.route('/', methods=['GET', 'POST'])
def new_article():
    if session['login'] != 'true':
        return '<h1>Under construction</h1>'
    f = forms.NewPostForm()
    if f.validate_on_submit():
        post = Article(title=f.title.data,
                       subtitle=f.subtitle.data,
                       content=markdown_to_html(f.content.data),
                       image_url=f.image_url.data,
                       timestamp=datetime.utcnow())
        if f.formatted_title.data:
            post.formatted_title = f.formatted_title.data
        tags = f.tags.data.split(', ')
        for t in tags:
            altag = Tag.query.filter_by(tagname=t).first()
            if altag:
                altag.articles.append(post)
                db.session.add(altag)
            else:
                db.session.add(Tag(tagname=t, articles=[post]))
        db.session.add(post)
        return redirect(url_for('main.article_page', num=post.id))
    return render_template('new-article.html', form=f)


@admin.route('/<int:num>', methods=['GET', 'POST', 'DELETE'])
def manage_article(num):
    if session['login'] != 'true':
        return '<h1>Under construction</h1>'
    f = forms.NewPostForm()
    article = Article.query.filter_by(id=num).first()
    if f.validate_on_submit():
        article.title = f.title.data
        article.subtitle = f.subtitle.data
        article.content = f.content.data
        article.image_url = f.image_url.data
        if f.formatted_title.data:
            article.formatted_title = f.formatted_title.data
        for t in article.tags:
            altag = Tag.query.filter_by(tagname=t).first()
            altag.articles.remove(article)
        tags = f.tags.data.split(', ')
        for t in tags:
            altag = Tag.query.filter_by(tagname=t).first()
            if altag:
                altag.articles.append(post)
                db.session.add(altag)
            else:
                db.session.add(Tag(tagname=t, articles=[post]))
        db.session.add(article)
        return redirect(url_for('main.article_page', num=num))
    f.title.data = article.title
    f.subtitle.data = article.subtitle
    f.formatted_title.data = article.formatted_title
    f.content.data = article.content
    f.image_url.data = article.image_url
    f.tags.data = ', '.join(article.tags)

    return render_template('new-article.html', form=f)



@admin.route('/login', methods=['GET', 'POST'])
def login_page():
    f = forms.LoginForm()
    session['login'] = None
    app = current_app._get_current_object()
    if f.validate_on_submit():
        if f.password.data == app.config['BLOG_PASSWD'] and app.config['BLOG_ADMIN'] == f.name.data:
            session['login'] = 'true'
        return redirect(url_for('admin.new_article'))
    return render_template('login.html', form=f)

