import unittest

from app.main.service.household_service import create_new_household
from app.test.base import BaseTestCase

household_with_member_data = {
    "household_id": 0,
    "type": 1,
    "members": [
        {
            "nric": "S9909757I",
            "name": "Eric Lee",
            "gender": 1,
            "dob": "1992-05-15",
            "annual_income": 123987,
            "occupation_type": 1,
            "marital_status": 1,
            "spouse_nric": "S9909758I"
        },
        {
            "nric": "S9909758I",
            "name": "Yan Ni",
            "gender": 1,
            "dob": "1994-05-15",
            "annual_income": 123987,
            "occupation_type": 1,
            "marital_status": 1,
            "spouse_nric": "S9909757I"
        }
    ]
}
class TestHouseholdController(BaseTestCase):
    def test_vaid_create_new_household_without_member(self):
        """ Test creating valid new household without members inside """
        data = {
            "type": 1
        }
        response_object, status_code = create_new_household(data)
        self.assertEqual(status_code, 201)
        success_response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        self.assertEqual(response_object, success_response_object)

    def test_valid_create_new_household_with_member(self):
        """ Test creating valid new household with members inside """
        response_object, status_code = create_new_household(household_with_member_data)
        self.assertEqual(status_code, 201)
        success_response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        self.assertEqual(response_object, success_response_object)

    def test_invaid_create_new_household_with_member(self):
        """ Test creating invalid new household with members inside """
        self.test_valid_create_new_household_with_member()
        response_object, status_code = create_new_household(household_with_member_data)
        self.assertEqual(status_code, 409, "Duplicate insertion of member")


if __name__ == '__main__':
    unittest.main()
