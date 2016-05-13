import unittest
from flask import url_for
from app import create_app, db
from app.models import Article, Comment, Tag


class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_homepage(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('I still love you, Ahoo' in response.get_data(as_text=True))


        
