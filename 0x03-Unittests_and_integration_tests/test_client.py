#!/usr/bin/env python3
"""
A Test module
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    A test class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Method to test GithubOrgClient.org
        """
        # Create an instance of GithubOrgClient with the org_name
        github_client = GithubOrgClient(org_name)

        # Set the return value for the mocked get_json method
        mock_get_json.return_value = {"name": org_name, "description": "Test Org"}

        # Access the org property instead of calling the org method directly
        result = github_client.org

        # Assert that get_json is called once with the expected argument
        mock_get_json.assert_called_once_with(GithubOrgClient.ORG_URL.format(org=org_name))

        # Assert that the result is correct
        self.assertEqual(result, {"name": org_name, "description": "Test Org"})

    @patch("client.get_json")
    def test_public_repos_url(self, mock_get_json):
        """
        To test GithubOrgClient._public_repos_url
        """
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Mock the response from GithubOrgClient.org
        mock_get_json.return_value = {
            "name": "test_org",
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        # Access the _public_repos_url property
        result = github_client._public_repos_url

        # Assert that GithubOrgClient.org is called once
        mock_get_json.assert_called_once()

        # Assert that the result is the
        # expected repos_url from the mock payload
        self.assertEqual(result, "https://api.github.com/orgs/test_org/repos")


if __name__ == "__main__":
    unittest.main()
