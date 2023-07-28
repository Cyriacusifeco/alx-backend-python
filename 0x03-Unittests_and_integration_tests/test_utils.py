#!/usr/bin/env python3
"""
A Test Module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """
    A Test class for the nestedMap function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"]),
    ])
    def test_access_nested_map_exception(self, map, path):
        """ Test that keyErrors are raised for invalid key"""
        with self.assertRaises(KeyError):
            result = access_nested_map(map, path)


class TestGetJson(unittest.TestCase):
    """ Test class for get_json function """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """ Mock the requests.get method """
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """A class to test memoization
    """

    def test_memoize(self):
        """
        Test method.
        """
        # Define the TestClass inside the test_memoize method
        class TestClass:
            """
            Sample class to be tested.
            """
            def a_method(self):
                """
                Simple method to be called
                """
                return 42

            @memoize
            def a_property(self):
                """
                Exact method to be tested for memoization.
                """
                return self.a_method()

        # Create an instance of TestClass
        test_instance = TestClass()

        # Mock the a_method of TestClass
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Set the return value for the mocked method
            mock_a_method.return_value = 42

            # Call the a_property method twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that a_method is called only once
            mock_a_method.assert_called_once()

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == "__main__":
    unittest.main()
