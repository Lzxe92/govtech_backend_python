import operator

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


def get_all_household_student_with_filter(request=None):
    "Fulfills the following criteria"
    "1.Households with children of less than {age} years old"
    "2.Household income of less than ${total_income}."
    household_list = []
    if "age" in request:
        less_than_age_list = set()
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            filter(
            cmp(func.TIMESTAMPDIFF(sqlalchemy.text('YEAR'), Member.dob, sqlalchemy.text('CURDATE()')),
                request["age"]["operator"],
                request["age"]["value"]))
        for household in result.all():
            less_than_age_list.add(household)
        household_list.append(less_than_age_list)

    if "total_income" in request:
        total_income_list = set()
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            group_by(Household.household_id).having(
            cmp(func.sum(Member.annual_income),
                request["total_income"]["operator"],
                request["total_income"]['value']))
        for household in result.all():
            total_income_list.add(household)
        household_list.append(total_income_list)

    if not household_list:
        return []
    result = household_list[0]
    for household in household_list:
        result = result.intersection(household)
    return list(result)


ops = {
    '<': operator.lt,
    '>': operator.gt,
    # '<=': operator.le,
    # '==': operator.eq,
    # '!=': operator.ne,
    # '>=': operator.ge,
}


def cmp(arg1, op, arg2):
    operation = ops.get(op)
    return operation(arg1, arg2)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
