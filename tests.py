import unittest, json
from database.source import Database
from database.exceptions import *

EMPTY_LENGTH = 0


class TestDatabase(unittest.TestCase):
    """
        Test class to make insure Database works as expected
    """

    def setUp(self) -> None:
        self.user_db = Database().connect(source='data/users.json')
        self.ticket_db = Database().connect(source='data/tickets.json')
        self.organization_db = Database().connect(source='data/organizations.json')

    def test_get_fields(self):
        """Test to make sure that fields could retrieved successfully"""
        self.assertNotEqual(len(self.user_db.fields()), EMPTY_LENGTH)
        self.assertNotEqual(len(self.ticket_db.fields()), EMPTY_LENGTH)
        self.assertNotEqual(len(self.organization_db.fields()), EMPTY_LENGTH)

    def test_get_fields_db_not_connected(self):
        """Test to make sure the proper exception is raised when db is not connected"""
        # before accessing db.field(), db.connect(path) method should be called
        db = Database()
        with self.assertRaises(DatabaseIsNotConnectedError):
            db.fields()

    def test_filter_string_value(self):
        """Test to make sure filter works successfully for string values"""

        query_result = [
            self.user_db.filter('url', "http://initech.aiworks.com/api/v2/users/1.json"),
            self.organization_db.filter('external_id', "9270ed79-35eb-4a38-a46f-35725197ea8d"),
            self.ticket_db.filter('status', 'hold')
        ]

        for result in query_result:
            self.assertNotEqual(len(result), EMPTY_LENGTH)

    def test_filter_integer_value(self):
        """Test to make sure filter works successfully for integer values"""

        query_result = [
            self.user_db.filter('_id', 5),
            self.organization_db.filter('_id', 101),
            self.ticket_db.filter('submitter_id', 38)
        ]

        for result in query_result:
            self.assertNotEqual(len(result), EMPTY_LENGTH)

    def test_filter_bool_value(self):
        """Test to make sure filter works successfully for bool values"""

        query_result = [
            self.user_db.filter('active', True),
            self.organization_db.filter('shared_tickets', False),
            self.ticket_db.filter('has_incidents', False)
        ]

        for result in query_result:
            self.assertNotEqual(len(result), EMPTY_LENGTH)

    def test_filter_list_value(self):
        """
            Test to make sure filter works successfully when there is the matched
            value in the list
        """

        query_result = [
            self.user_db.filter('tags', "Roberts"),
            self.organization_db.filter('domain_names', 'dadabase.com'),
            self.ticket_db.filter('tags', "Nevada")
        ]

        for result in query_result:
            self.assertNotEqual(len(result), EMPTY_LENGTH)

    def test_filter_get_value(self):
        """Test to make sure to get only matched item"""

        query_result = [
            self.user_db.get('_id', 9),
            self.organization_db.get('domain_names', 'dadabase.com'),
            self.ticket_db.get('assignee_id', 7)
        ]

        for result in query_result:
            self.assertEqual(type(result), dict)

    def test_empty_values(self):
        """Test to make sure there is no value when the search is not satisfied"""
        result = self.user_db.filter('tags', "this_term_not_exist")
        self.assertEqual(len(result), EMPTY_LENGTH)

    def test_field_not_found(self):
        """
            Test to make sure an appropriate exception is raised when the field doesn't
            exist
        """
        with self.assertRaises(FieldNotFoundError):
            self.user_db.filter('bad_field', 2)

    def test_data_invalid_not_found(self):
        """
            Test to make sure an appropriate exception is raised when the data doesn't
            have the right format
        """
        with self.assertRaises(DataIsNotJSONError):
            Database().connect(source=(2, 5))
