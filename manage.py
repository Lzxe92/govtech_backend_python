import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint

from app.main import create_app, db
from database.seed_tables import seed_tables

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
app.register_blueprint(blueprint)

app.app_context().push()


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed():
    seed_tables()


if __name__ == '__main__':
    manager.run()
