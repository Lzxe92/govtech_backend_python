from flask import request
from ..util.household_dto import HouseholdDto
from ..service.household_service import *
from flask_restx import Api, Resource, fields

api = HouseholdDto.api
_household = HouseholdDto.household


@api.route('/')
class HouseholdList(Resource):
    @api.doc('list_of_household')
    @api.marshal_list_with(_household)
    def get(self):
        """List all Household"""
        return get_all_household()

    @api.response(201, 'Household successfully created.')
    @api.doc('create a new household')
    @api.expect(_household, validate=True)
    def post(self):
        """Creates a new Household """
        data = request.json
        return create_new_household(data)


@api.route('/<int:household_id>/member/<int:member_id>')
@api.param('household_id', 'The Household identifier')
@api.param('member_id', 'The Member identifier')
class HouseholdList(Resource):
    @api.response(201, 'Member added to household.')
    @api.doc('add household to member')
    def post(self, household_id, member_id):
        """Add member into household """
        return create_new_household_member(household_id, member_id)


@api.route('/<int:household_id>')
@api.param('household_id', 'The Household identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a household')
    @api.marshal_with(_household)
    def get(self, household_id):
        """get a Household given its identifier"""
        household = get_a_household(household_id)
        if not household:
            api.abort(404)
        else:
            return household


@api.route('/search')
@api.doc(params=
         {'age': {'description': 'Less than the age', 'in': 'query', 'type': 'int'},
          'total_income': {'description': 'Total household income less than the specified amount',
                           'in': 'query',
                           'type': 'float'}
          })
class Household(Resource):
    @api.marshal_list_with(_household)
    def get(self, ):
        """get Households and filter by search parameters"""
        data = {}

        # Transforming all request into search parameters
        allowed_fillters = ["age","total_income"]
        for item in request.args:
            # filtering allowed parameters for search
            if item not in allowed_fillters:
                continue
            if request.args.get(item):
                if not transform_parameter(request.args.get(item)):
                    api.abort(400)
                data[item] = transform_parameter(request.args.get(item))
        result = get_all_household_student_with_filter(data)
        return result


def transform_parameter(param):
    data = {"value": None, "operator": None}
    opeartor = {'<', '>'}
    try:
        if param[:1] not in opeartor:
            return None
        if not param[1:].isdigit():
            return None
        data["operator"] = param[:1]
        data["value"] = param[1:]
    except:
        print("An exception occurred")
    return data
