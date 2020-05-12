from app.main import db
from app.main.model.Member import Member


def create_new_member(data):
    nric = data.get("nric", None)
    member = Member.query.filter_by(nric=nric).first()
    # # check if spouse exists, if not return 400 for invalid spouse_nric
    # spouse_nric = data.get("spouse_nric", None)
    # if spouse_nric:
    #     spouse = Member.query.filter_by(nric=spouse_nric).first()
    #     if not spouse:
    #         response_object = {
    #             'status': 'fail',
    #             'message': 'spouse not found.'
    #         }
    #         return response_object, 400

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
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Member already exists.',
        }
        return response_object, 409


def get_all_member():
    return Member.query.all()


def get_a_member(member_id):
    return Member.query.filter_by(member_id=member_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
