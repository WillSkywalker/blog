from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request
from num2words import num2words
from hashlib import md5
from markdown import markdown
import bleach


from . import main, forms
from .. import db
from ..models import Article, Tag, Comment


ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']


def markdown_to_html(value):
    return bleach.linkify(bleach.clean(markdown(value, output_format='html'), 
                                tags=ALLOWED_TAGS, strip=True))


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the "%s" field - %s' % (
                getattr(form, field).label.text,
                error
            ))


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
    taglist = filter(lambda x: x.articles.count() > 1, Tag.query.all())
    taglist = list(sorted(taglist, key=lambda x: x.articles.count(), reverse=True))
    return render_template('tags-list.html', tags=taglist)


@main.route('/message', methods=['GET', 'POST'])
@main.route('/message/<int:page>', methods=['GET', 'POST'])
def contact(page=1):
    f = forms.CommentForm()
    if f.validate_on_submit():
        message = Comment(name=f.name.data,
                          email=f.email.data,
                          content=markdown_to_html(f.comment.data),
                          timestamp=datetime.utcnow(),
                          md5=md5(f.email.data.encode('utf-8')).hexdigest(),
                          of_article=0)
        if is_valid_url(f.homepage.data):
            message.homepage = f.homepage.data
        db.session.add(message)
        return redirect(url_for('main.contact'))
    if request.method == 'POST':
        flash_errors(f)
        return redirect(url_for('main.contact'))

    manage = False
    if 'login' in session and session['login'] == 'true':
        manage = True
    pagination = Comment.query.filter_by(of_article=0).order_by(-Comment.id)\
        .paginate(page, per_page=50, error_out=False)
    return render_template('contact.html', pagination=pagination, form=f, manage=manage)


@main.route('/search')
def search():
    return render_template('search.html')


@main.route('/me')
def aboutme():
    return render_template('about.html')

