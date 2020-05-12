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
        # data = api.payload
        return create_new_household(data)


@api.route('/<household_id>/member/<member_id>')
@api.param('household_id', 'The Household identifier')
@api.param('member_id', 'The Member identifier')
class HouseholdList(Resource):
    @api.response(201, 'Member added to household.')
    @api.doc('add household to member')
    def post(self, household_id, member_id):
        """Creates a new Household """
        # data = api.payload
        return create_new_household_member(household_id, member_id)


@api.route('/<household_id>')
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
