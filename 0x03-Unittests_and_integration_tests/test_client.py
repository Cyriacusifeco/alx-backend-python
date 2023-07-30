#!/usr/bin/env python3
"""
A Test module
"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Mock the response from GithubOrgClient.org
        mock_get_json.return_value = {
            "name": "test_org",
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        # Mock the response from GithubOrgClient.repos_payload
        mock_repos_payload = MagicMock()
        mock_repos_payload.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]

        with patch.object(GithubOrgClient, 'repos_payload', mock_repos_payload):
            # Call the public_repos method
            repos = github_client.public_repos(license="mit")

        # Assert that GithubOrgClient.org is called once
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org")

        # Assert the list of repos is what we expect from the chosen payload
        expected_repos = ["repo1", "repo3"]
        self.assertEqual(repos, expected_repos)

    @patch("client.get_json")
    def test_has_license(self, mock_get_json):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Mock the response from GithubOrgClient.org
        mock_get_json.return_value = {
            "name": "test_org",
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        # Test cases with different inputs and expected results
        test_cases = [
            # repo={"license": {"key": "my_license"}}, license_key="my_license"
            {
                "repo": {"license": {"key": "my_license"}},
                "license_key": "my_license",
                "expected_result": True,
            },
            # repo={"license": {"key": "other_license"}}, license_key="my_license"
            {
                "repo": {"license": {"key": "other_license"}},
                "license_key": "my_license",
                "expected_result": False,
            },
        ]

        for case in test_cases:
            repo = case["repo"]
            license_key = case["license_key"]
            expected_result = case["expected_result"]

            # Call the has_license method with the given input
            result = github_client.has_license(repo, license_key)

            # Assert the returned value is as expected
            self.assertEqual(result, expected_result)


@parameterized_class(
        ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
        fixtures.TEST_PAYLOAD
        )
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Patch requests.get to return example payloads from fixtures
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure the side_effect of mock_get to return the correct fixtures
        cls.mock_get.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.repos_payload,
            cls.repos_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        # Stop the patcher after the tests are done
        cls.get_patcher.stop()

    def test_public_repos(self):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Call the public_repos method with license="mit"
        repos = github_client.public_repos(license="mit")

        # Assert the list of repos is what we expect from the chosen payload
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license_key(self):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Call the public_repos method with license="apache-2.0"
        repos = github_client.public_repos(license="apache-2.0")

        # Assert the list of repos is what we expect from the chosen payload
        self.assertEqual(repos, self.apache2_repos)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    fixtures.TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Patch requests.get to return example payloads from fixtures
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure the side_effect of mock_get to return the correct fixtures
        cls.mock_get.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.repos_payload,
            cls.repos_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        # Stop the patcher after the tests are done
        cls.get_patcher.stop()

    def test_public_repos(self):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Call the public_repos method with license="mit"
        repos = github_client.public_repos(license="mit")

        # Assert the list of repos is what we expect from the chosen payload
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        # Create an instance of GithubOrgClient with a dummy org_name
        github_client = GithubOrgClient("test_org")

        # Call the public_repos method with license="apache-2.0"
        repos = github_client.public_repos(license="apache-2.0")

        # Assert the list of repos is what we expect from the chosen payload
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
