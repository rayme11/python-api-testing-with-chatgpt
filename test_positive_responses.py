# /tests/test_positive_responses.py
import unittest
from config import setup, API_KEY, URL
import requests


class TestPositiveResponses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Retrieve the API key from environment variables
        cls.api_key = API_KEY

        # Define the API endpoint
        cls.url = URL

        # Call the setup function and check for connection
        try:
            setup()
        except ConnectionError as e:
            print(f"Setup failed: {e}")
            cls.skipTest("Skipping tests due to failed API connection.")

    def test_some_positive_response(self):
        # Write your test case here
        params = {
            "q": "London",  # The city to query
            "appid": self.api_key  # The API key
        }

        # Make the API request
        response = requests.get(self.url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            print("Connection and first test was ok !!")
            weather_data = response.json()
            print(weather_data)


if __name__ == "__main__":
    unittest.main()
