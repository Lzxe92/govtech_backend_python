from flask_restx import Namespace, fields


class MemberDto:
    api = Namespace('member', description='member related operations')
    member = api.model('member', {
        'member_id': fields.Integer(required=False, description='Identifier of the member'),
        'nric': fields.String(required=True, min=9, max=9, description='NRIC of the member, EG. S9209759I'),
        'name': fields.String(required=True, description='name of the member'),
        'gender': fields.Integer(
            required=True,
            description='1= male, 2=female',
            min=1,
            max=2
        ),
        'dob': fields.Date(required=True, description='DOB of the member'),
        'annual_income': fields.Float(required=True, description='Annual income of the member'),
        'occupation_type': fields.Integer(
            required=False,
            description='0= Unemployed, 1= Student, 2=Employed',
            default=0,
            min=0,
            max=2
        ),
        'marital_status': fields.Integer(
            required=False,
            description='0= not married, 1= married',
            default=0,
            min=0,
            max=2
        ),
        'spouse_nric': fields.String(
            required=False,
            default=None,
            description='nric of spouse',
            min=9,
            max=9
        )
    })
