import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    f = list(map(lambda x:x.rstrip(), open('.secrets').readlines())) or None
    SECRET_KEY = f[0] or 'kuchtopatazindagis'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BLOG_ADMIN = f[1] or os.environ.get("BLOG_ADMIN")
    BLOG_PASSWD = f[2] or os.environ.get('BLOG_PASSWD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    FREEZER_BASE_URL = '/blog'


    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    SECRET_KEY = 'Te apuntaste al DELE de mayo'
    BLOG_ADMIN = 'test'
    BLOG_PASSWD = '1234'
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 
                                                          'test_data.sqlite')



config = {
    'default': Config,
    'testing': TestConfig,
}
