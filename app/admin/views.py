from flask import render_template, session, redirect, url_for
from . import admin, forms
from ..models import Article, Tag
from .. import db
from os import environ
from datetime import datetime


@admin.route('/', methods=['GET', 'POST'])
def new_article():
    f = forms.NewPostForm()
    if session['login'] != 'true':
        return '<h1>Under construction</h1>'
    if f.validate_on_submit():
        post = Article(title=f.title.data,
                       subtitle=f.subtitle.data,
                       content=f.content.data,
                       image_url=f.image_url.data,
                       viewcount=0,
                       timestamp=datetime.utcnow())
        tags = f.tags.data.split(', ')
        for t in tags:
            altag = Tag.query.filter_by(tagname=t).first()
            if altag:
                altag.articles.add(post)
            else:
                print('Tag %s not exist' % t)
        db.session.add(post)
        return redirect(url_for('main.index'))
    return render_template('new-article.html', form=f)


@admin.route('/<int:num>', methods=['GET', 'POST', 'DELETE'])
def manage_article(num):
    if session['login'] != 'true':
        return '<h1>Under construction</h1>'
    return render_template('manage.html')


@admin.route('/login', methods=['GET', 'POST'])
def login_page():
    f = forms.LoginForm()
    session['login'] = None
    if f.validate_on_submit():
        if f.password.data == environ['BLOG_PASSWD'] and environ['BLOG_ADMIN'] == f.name.data:
            session['login'] = 'true'
        return redirect(url_for('admin.new_article'))
    return render_template('login.html', form=f)