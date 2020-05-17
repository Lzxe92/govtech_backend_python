import unittest
import json
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


def register_household_without_member(self):
    return self.client.post(
        '/household/',
        data=json.dumps(dict(
            type=2,
        )),
        content_type='application/json'
    )


def register_household_with_member(self):
    return self.client.post(
        '/household/',
        data=json.dumps(household_with_member_data),
        content_type='application/json'
    )


class TestHouseholdController(BaseTestCase):

    def test_valid_create_household_without_member(self):
        """ Test of creating household using rest call   """
        with self.client:
            # Creating household
            result = register_household_without_member(self)
            self.assertEqual(result.status_code, 201)

    def test_valid_create_household_with_member(self):
        """ Test of creating household using rest call   """
        with self.client:
            # Creating household with member
            result = register_household_with_member(self)
            self.assertEqual(result.status_code, 201)


if __name__ == '__main__':
    unittest.main()
