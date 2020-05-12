from flask_restx import Namespace, fields


class HouseholdDto:
    api = Namespace('household', description='household related operations')
    household = api.model('household', {
        'household_id': fields.Integer(required=False, description='Identifier of the household'),
        'type': fields.Integer(
            required=True,
            description='housing type, 1= HDB, 2=Condo, 3= Landed',
            min=0,
            max=4
        )
    })
