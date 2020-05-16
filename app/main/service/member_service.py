from sqlalchemy import or_

from app.main import db
from app.main.model.Member import Member
from app.main.util.wrapper import create_service_response


def create_new_member(data):
    nric = data.get("nric", None)
    member = Member.query.filter_by(nric=nric).first()

    if not member:
        new_member = Member(
            nric=nric,
            name=data.get("name", 0),
            gender=data["gender"],
            dob=data.get("dob", None),
            annual_income=data.get("annual_income", 0),
            occupation_type=data.get("occupation_type", 0),
            marital_status=data.get("marital_status", 0),
            spouse_nric=data.get("spouse_nric", None)
        )
        save_changes(new_member)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return create_service_response(new_member, response_object, 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Member already exists.',
        }
        return create_service_response(None, response_object, 409)


def get_all_member():
    return Member.query.all()


def get_a_member(member_id):
    return Member.query.filter_by(member_id=member_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


# validate no duplicates for member insertion
def validate_members_insertion(data):
    member_nric_list = []
    member_spouse_id_list = []
    for member in data:
        if member["nric"]:
            member_nric_list.append(member["nric"])
        if member["spouse_nric"]:
            member_spouse_id_list.append(member["spouse_nric"])
    result = db.session.query(Member).filter(or_(
        Member.nric.in_(member_nric_list),
        Member.spouse_nric.in_(member_spouse_id_list)
    )
    ).all()
    return result
