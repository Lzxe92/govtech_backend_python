from flask_restx import Namespace, fields

from app.main.util.member_dto import MemberDto


class HouseholdDto:
    api = Namespace('household', description='household related operations')
    member = MemberDto.member
    household = api.model('household', {
        'household_id': fields.Integer(required=False, description='Identifier of the household'),
        'type': fields.Integer(
            required=True,
            description='housing type, 1= HDB, 2=Condo, 3= Landed',
            min=1,
            max=3,
            default=1
        ),
        'members': fields.List(
            fields.Nested(member, required=False)
        )
    })
