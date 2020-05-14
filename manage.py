import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint

from app.main import create_app, db
from app.main.model.Household import Household
from app.main.model.Member import Member

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
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
    # Create five household
    household_list = []
    household_list.append(Household(type=1))
    household_list.append(Household(type=1))
    household_list.append(Household(type=1))
    household_list.append(Household(type=2))
    household_list.append(Household(type=3))
    for household in household_list:
        db.session.add(household)

    # Create 10 Member
    household_list[0].members.append(Member(
        nric="S0910101Z",
        name="Lee Ah Bah",
        gender=1,
        dob="1958-05-21",
        annual_income=41600,
        occupation_type=0,
        marital_status=1,
        spouse_nric="S0910139Z"
    ))

    household_list[0].members.append(Member(
        nric="S0910102Z",
        name="Lilis",
        gender=2,
        dob="1965-05-21",
        annual_income=51600,
        occupation_type=2,
        marital_status=1,
        spouse_nric="S0910139Z"
    ))

    household_list[0].members.append(Member(
        nric="S9209703I",
        name="Eric Lee",
        gender=1,
        dob="1992-03-14",
        annual_income=80000,
        occupation_type=2,
        marital_status=0
    ))

    household_list[0].members.append(Member(
        nric="S910104Z",
        name="Joan Lee",
        gender=2,
        dob="1991-05-21",
        annual_income=80000,
        occupation_type=2,
        marital_status=0
    ))

    household_list[1].members.append(Member(
        nric="S0910105Z",
        name="Person 5",
        gender=1,
        dob="2017-05-21",
        annual_income=0,
        occupation_type=0,
        marital_status=0,
        spouse_nric=None
    ))

    household_list[1].members.append(Member(
        nric="S0910106Z",
        name="Person 6",
        gender=1,
        dob="1965-05-21",
        annual_income=510600,
        occupation_type=2,
        marital_status=1,
        spouse_nric="S0910109Z"
    ))

    household_list[2].members.append(Member(
        nric="S0910107Z",
        name="Person 7",
        gender=1,
        dob="2017-05-21",
        annual_income=0,
        occupation_type=0,
        marital_status=0,
        spouse_nric=None
    ))

    household_list[2].members.append(Member(
        nric="S0910108Z",
        name="Person 8",
        gender=2,
        dob="1965-05-21",
        annual_income=510600,
        occupation_type=2,
        marital_status=1,
        spouse_nric="S0910107Z"
    ))

    household_list[3].members.append(Member(
        nric="S0910109Z",
        name="Person 9",
        gender=1,
        dob="1965-05-21",
        annual_income=510600,
        occupation_type=2,
        marital_status=0
    ))

    household_list[4].members.append(Member(
        nric="S0910110Z",
        name="Person 10",
        gender=2,
        dob="1965-05-21",
        annual_income=610600,
        occupation_type=2,
        marital_status=0
    ))

    db.session.commit()

    print("Records seeded")


if __name__ == '__main__':
    manager.run()
