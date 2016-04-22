import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BLOG_ADMIN = os.environ.get("BLOG_ADMIN")
    BLOG_PASSWD = os.environ.get('BLOG_PASSWD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 
                                                          'test_data.sqlite')



config = {
    'default': Config,
    'test': TestConfig,
}
