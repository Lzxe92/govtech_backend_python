from flask import request
from flask_restx import Resource

from ..util.member_dto import MemberDto
from ..service.member_service import *
from flask_restx import Api, Resource, fields

api = MemberDto.api
_member = MemberDto.member


@api.route('/')
class MemberList(Resource):
    @api.doc('list_of_member')
    @api.marshal_list_with(_member)
    def get(self):
        """List all Member"""
        return get_all_member()

    @api.response(201, 'Member successfully created.')
    @api.doc('create a new Member')
    @api.expect(_member, validate=True)
    def post(self):
        """Creates a new Member """
        data = request.json
        # data = api.payload
        return create_new_member(data)


@api.route('/<member_id>')
@api.param('member_id', 'The Member identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a member')
    @api.marshal_with(_member)
    def get(self, member_id):
        print(member_id)
        """get a Household given its identifier"""
        member = get_a_member(member_id)
        if not member:
            api.abort(404)
        else:
            return member
