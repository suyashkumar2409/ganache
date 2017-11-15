#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Request, Quiz, Score, init, AudioFile, savePkl, loadPkl
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Request = Request, Quiz = Quiz, Score = Score, AudioFile = AudioFile, savePkl = savePkl, loadPkl = loadPkl)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# manager.add_command('runserver', Server(host="0.0.0.0", port=9000))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
	init()
	manager.run()
