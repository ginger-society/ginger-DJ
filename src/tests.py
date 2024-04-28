from ginger.test import TestCase

# Create your tests here.
"""tests for api_server"""
import json

from ginger.test import Client, TestCase


client = Client()


class HealthCheck(TestCase):
    """
    checks if the server is booted
    """

    def test_is_healthy(self):
        """it should respond with {status : 'ok'}"""
        response = client.get("/admin")
        self.assertEqual(response.status_code, 301)