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

    household_member = HouseholdMember.query.filter_by(member_id=member_id).first()
    if household_member:
        response_object = {
            'status': 'fail',
            'message': 'Member is already in a household. (one member can only be in one household)',
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

""" 
delete all members found from the household from the database and also delete the household from database
remove the association in the process
"""
def delete_household_and_members(household_id):
    household = Household.query.filter_by(household_id=household_id).first()
    if not household:
        response_object = {
            'status': 'fail',
            'message': 'Household id given is not found.'
        }
        return response_object, 404
    db.session.delete(household)
    for member in household.members:
        db.session.delete(member)
    db.session.commit()
    # delete successful, 204 no content
    return {}, 204


def get_all_household_student_with_filter(request=None):
    household_list = []
    # Search filter
    if "age" in request:
        less_than_age_set = set()
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            filter(
            cmp(func.TIMESTAMPDIFF(sqlalchemy.text('YEAR'), Member.dob, sqlalchemy.text('CURDATE()')),
                request["age"]["operator"],
                request["age"]["value"]))
        for household in result.all():
            less_than_age_set.add(household)
        household_list.append(less_than_age_set)

    #total_income filter
    if "total_income" in request:
        total_income_set = set()
        result = db.session.query(Household). \
            join(*Household.members.attr). \
            group_by(Household.household_id).having(
            cmp(func.sum(Member.annual_income),
                request["total_income"]["operator"],
                request["total_income"]['value']))
        for household in result.all():
            total_income_set.add(household)
        household_list.append(total_income_set)
    """ 
    Households with husband & wife 
    Using raw query instead of orm 
    to hit the criteria, both husband and wife must have their spouse_nric belong to the opposing party
    marital_status request parameter to be set as eq1
    """
    if "marital_status" in request and \
            request["marital_status"]["value"] == "1" and \
            request["marital_status"]["operator"] == "eq":
        marrital_status_set = set()

        result = db.engine.execute(
            "select household.household_id from member "
            "INNER join household_member on member.member_id = household_member.member_id  "
            "INNER join household on household_member.household_id = household.household_id "
            "inner join member m2 on member.spouse_nric = m2.spouse_nric "
            "where member.marital_status=1 "
            "GROUP BY household.household_id "
            "having count(household.household_id) >=2")

        married_house_hold_list = [row[0] for row in result]
        result = db.session.query(Household).filter(Household.household_id.in_(married_house_hold_list))
        for household in result.all():
            marrital_status_set.add(household)
        household_list.append(marrital_status_set)
    """ 
    Households Type search critera 
    usng orm to filter and get the housetype based on the parameter household_type 
    EG household_type=eq1, means household with type =1
    """
    if "household_type" in request and request["household_type"]["value"]:
        result = Household.query.filter_by(type=request["household_type"]["value"])
        household_type_set = set()
        for household in result.all():
            household_type_set.add(household)
        print(household_type_set)
        household_list.append(household_type_set)

    if not household_list:
        return []
    result = household_list[0]
    for household in household_list:
        result = result.intersection(household)
    return list(result)

""" 
delete memeber from household. It remove the association in household_member.
It does not delete member from the database.
"""
def delete_member_from_household(household_id, member_id):
    household_member = HouseholdMember.query.filter_by(household_id=household_id, member_id=member_id).first()
    if not household_member:
        response_object = {
            'status': 'fail',
            'message': 'Member not found in the household.',
        }
        return response_object, 404
    db.session.delete(household_member)
    db.session.commit()
    return {}, 204


opeartor = {
    'lt': operator.lt,
    'gt': operator.gt,
    'le': operator.le,
    'eq': operator.eq,
    'ne': operator.ne,
    'ge': operator.ge,
}


def cmp(arg1, op, arg2):
    operation = opeartor.get(op)
    return operation(arg1, arg2)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
