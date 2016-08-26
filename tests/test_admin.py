import unittest
from flask import url_for, session
from app import create_app, db
from app.models import Article, Comment, Tag


class TestAdmin(unittest.TestCase):

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


    def test_login(self):
        self.client.get(url_for('admin.login_page'))
        response = self.client.post(url_for('admin.login_page'), data={
            'name': 'test',
            'password': '1234'
            }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bernie', response.get_data(as_text=True))

        response = self.client.post(url_for('admin.login_page'), data={
            'name': 'alice',
            'password': 'wonderland'
            }, follow_redirects=True)
        self.assertIn('Under construction', response.get_data(as_text=True))


    def test_new_article(self):
        self.client.post(url_for('admin.login_page'), data={
            'name': 'test',
            'password': '1234'
            })
        response = self.client.post(url_for('admin.new_article'), data={
            'title': 'A Day To Celebrate',
            'subtitle': 'Holiday Special!',
            'formatted_title': '<strong>A</strong> Day To Celebrate',
            'tags': 'The Lion, the Witch, the Wardrobe',
            'content': '##This is a test\n\nyes it is',
            'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/cb/The_Chronicles_of_Narnia_box_set_cover.jpg',
            }, follow_redirects=True)
        self.assertIn('<title>A Day To Celebrate - Will Skywalker\'s Ranch</title>', response.get_data(as_text=True))


    def test_manage_article(self):
        self.client.post(url_for('admin.login_page'), data={
            'name': 'test',
            'password': '1234'
            })
        response = self.client.post(url_for('admin.new_article'), data={
            'title': 'A Day To Celebrate',
            'subtitle': 'Holiday Special!',
            'tags': 'The Lion, the Witch, the Wardrobe',
            'content': '##This is a test\n\nyes it is',
            'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/cb/The_Chronicles_of_Narnia_box_set_cover.jpg',
            })
        self.client.get(url_for('admin.manage_article', num=1))
        response = self.client.post(url_for('admin.manage_article', num=1), data={
            'title': 'Another Day To Celebrate',
            'formatted_title': '<em>Another</em> Day To Celebrate',
            'subtitle': 'Holiday Special!',
            'tags': 'The Lion, the Witch, PCMR',
            'content': '##This is a test\n\nyes it is',
            'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/cb/The_Chronicles_of_Narnia_box_set_cover.jpg',
            }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('<a href="/blog/tag/the Wardrobe">the Wardrobe</a>', data)
        self.assertIn('<a href="/blog/tag/PCMR">PCMR</a>', data)
        self.assertIn('<h2><em>Another</em> Day To Celebrate</h2>', data)


        self.client.post(url_for('admin.login_page'), data={
            'name': 'test',
            'password': 'baaaaad'
            })
        self.assertIn('Under construction', 
            self.client.get(url_for('admin.manage_article', num=1)).get_data(as_text=True))


    def test_manage_comment(self):
        pass


        
