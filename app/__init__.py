from flask import Flask, render_template
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from config import config


moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

def create_app(config_name):
    from .main import main as main_bp
    from .admin import admin as admin_bp
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(main_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/blog/admin')


    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)

    return app
