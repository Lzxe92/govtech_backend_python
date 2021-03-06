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

    @api.response(204, 'Delete successful.')
    @api.response(404, 'Member not found in the household')
    def delete(self, household_id, member_id):
        """Remove Family Member from the Household. """
        return delete_member_from_household(household_id, member_id)


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

    @api.doc('delete and members inside')
    @api.response(204, 'Delete successful.')
    @api.response(404, 'Household not found.')
    def delete(self, household_id):
        result = delete_household_and_members(household_id)
        return result


@api.route('/search')
@api.doc(params=
         {'age': {'description': 'search parameter for a member in a household wit age, eg. lt29 (Less than 29)',
                  'in': 'query', 'type': 'string'},

          'total_income': {'description': 'search parameter for household income, eg. lt9000',
                           'in': 'query',
                           'type': 'string'},
          'marital_status': {'description': 'if there is a couple in same household, eg. eg1',
                             'in': 'query',
                             'type': 'string'},
          'household_type': {'description': 'type of the household, eg. eg1',
                             'in': 'query',
                             'type': 'string'}})
class Household(Resource):
    @api.marshal_list_with(_household)
    def get(self, ):
        """get Households and filter by search parameters"""
        data = {}

        # Transforming all request into search parameters
        allowed_request_filters = ["age", "total_income", "marital_status", "household_type"]
        for item in request.args:
            # filtering allowed parameters for search
            if item not in allowed_request_filters:
                continue
            if request.args.get(item):
                if not transform_parameter(request.args.get(item)):
                    api.abort(400)
                data[item] = transform_parameter(request.args.get(item))
        result = get_all_household_student_with_filter(data)
        return result


def transform_parameter(param):
    data = {"value": None, "operator": None}
    try:
        if param[:2] not in opeartor:
            return None
        if not param[2:].isdigit():
            return None
        data["operator"] = param[:2]
        data["value"] = param[2:]
    except:
        print("An exception occurred")
    return data
