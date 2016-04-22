#!/usr/bin/env python

import os
from app import create_app, db
from app.models import Article, Comment
from flask.ext.script import Shell, Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Article=Article, Comment=Comment)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
