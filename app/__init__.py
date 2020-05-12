# app/__init__.py

from flask_restx import Api
from flask import Blueprint

from .main.controller.household_controller import api as household_ns
from .main.controller.member_controller import api as member_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Govtech household appp',
          version='1.0',
          doc='/docs'
          )

api.add_namespace(household_ns)
api.add_namespace(member_ns)