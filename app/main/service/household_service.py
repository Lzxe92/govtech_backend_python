import sqlalchemy
from sqlalchemy import extract, func

from app.main import db
from app.main.model.Household import Household
from app.main.model.HouseholdMember import HouseholdMember
from app.main.model.Member import Member


def create_new_household(data):
    new_household = Household(
        type=data.get("type", 0)
    )
    save_changes(new_household)
    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return response_object, 201


def create_new_household_member(household_id, member_id):
    household = Household.query.filter_by(household_id=household_id).first()
    if not household:
        response_object = {
            'status': 'fail',
            'message': 'Household not found.',
        }
        return response_object, 404

    member = Member.query.filter_by(member_id=member_id).first()
    if not member:
        response_object = {
            'status': 'fail',
            'message': 'Member not found.',
        }
        return response_object, 404

    household_member = HouseholdMember.query.filter_by(household_id=household_id, member_id=member_id).first()
    if household_member:
        response_object = {
            'status': 'fail',
            'message': 'Member is already in the household.',
        }
        return response_object, 400

    household.members.append(member)
    save_changes(household)

    response_object = {
        'status': 'success',
        'message': 'Successfully added member {} to household.'.format(member.name)
    }
    return response_object, 201


def get_all_household():
    db.session
    return [
        {"household_id": 1, "type": 2,
         "members": [{"name": "wtf"}]}
    ]
    return Household.query.all()


def get_a_household(household_id):
    return Household.query.filter_by(household_id=household_id).first()


def get_all_household_student_with_filter(data=None):
    "Fulfills the following criteria"
    "1.Households with children of less than {age} years old"
    "2.Household income of less than ${total_income}."
    less_than_age_set = set()
    if data['age']:
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            filter(func.TIMESTAMPDIFF(sqlalchemy.text('YEAR'), Member.dob, sqlalchemy.text('CURDATE()')) <= data['age'])
        for household in result.all():
            less_than_age_set.add(household)

    less_than_income_set = set()
    if data['total_income']:
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            group_by(Household.household_id).having(func.sum(Member.annual_income) < data["total_income"])
        for household in result.all():
            less_than_income_set.add(household)
    return list(less_than_age_set & less_than_income_set)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
