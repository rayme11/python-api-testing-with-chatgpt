# /tests/test_positive_responses.py
import unittest
from config import setup, API_KEY, URL
import requests


class TestWeatherAPI(unittest.TestCase):

    def test_valid_coordinates(self):
        """Test with valid latitude and longitude"""
        params = {
            'lat': 44.34,
            'lon': 10.99,
            'appid': API_KEY,
            'units': 'imperial'  # Use 'imperial' units for Fahrenheit and mph
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('coord', data)
        self.assertIn('main', data)
        self.assertIn('weather', data)
        self.assertEqual(data['name'], 'Zocca')
        self.assertEqual(data['sys']['country'], 'IT')
        self.assertIsInstance(data['main']['temp'], float)
        self.expected_message = "Valid coordinates should return 200 status code and correct data."

    def test_invalid_coordinates(self):
        """Test with invalid latitude and longitude"""
        params = {
            'lat': -999,
            'lon': -999,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 400)  # Assuming the API returns 400 for invalid coordinates
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['cod'], '400')
        self.expected_message = "Invalid coordinates should return 400 status code and error message."

    def test_missing_api_key(self):
        """Test with missing API key"""
        params = {
            'lat': 44.34,
            'lon': 10.99,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 401)  # Assuming 401 Unauthorized for missing API key
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['cod'], 401)
        self.expected_message = "Missing API key should return 401 status code and error message."

    def test_invalid_api_key(self):
        """Test with invalid API key"""
        params = {
            'lat': 44.34,
            'lon': 10.99,
            'appid': 'invalid_api_key',
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 401)  # Assuming 401 Unauthorized for invalid API key
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['cod'], 401)
        self.expected_message = "Invalid API key should return 401 status code and error message."

    def test_max_latitude(self):
        """Test with maximum latitude (90)"""
        params = {
            'lat': 90,
            'lon': 0,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('coord', data)
        self.assertEqual(data['coord']['lat'], 90)
        self.expected_message = "Maximum latitude should return valid weather data."

    def test_min_latitude(self):
        """Test with minimum latitude (-90)"""
        params = {
            'lat': -90,
            'lon': 0,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('coord', data)
        self.assertEqual(data['coord']['lat'], -90)
        self.expected_message = "Minimum latitude should return valid weather data."

    def test_max_longitude(self):
        """Test with maximum longitude (180)"""
        params = {
            'lat': 0,
            'lon': 180,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('coord', data)
        self.assertEqual(data['coord']['lon'], 180)
        self.expected_message = "Maximum longitude should return valid weather data."

    def test_min_longitude(self):
        """Test with minimum longitude (-180)"""
        params = {
            'lat': 0,
            'lon': -180,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('coord', data)
        self.assertEqual(data['coord']['lon'], -180)
        self.expected_message = "Minimum longitude should return valid weather data."

    def test_temperature_extremes(self):
        """Test temperature extremes handling"""
        params = {
            'lat': 0,
            'lon': 0,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        temp_fahrenheit = data['main']['temp']
        self.assertGreaterEqual(temp_fahrenheit, -459.67)  # Fahrenheit cannot be below absolute zero
        self.expected_message = "Temperature should not be below absolute zero."

    def test_wind_speed_boundaries(self):
        """Test wind speed boundaries"""
        params = {
            'lat': 0,
            'lon': 0,
            'appid': API_KEY,
            'units': 'imperial'
        }
        response = requests.get(URL, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        wind_speed_mph = data['wind']['speed']
        self.assertGreaterEqual(wind_speed_mph, 0)  # Wind speed cannot be negative
        self.expected_message = "Wind speed should not be negative."


class TestResultTable(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TestResultTable, self).__init__(*args, **kwargs)
        self.test_results = []

    def addSuccess(self, test):
        super(TestResultTable, self).addSuccess(test)
        self.test_results.append((test, 'PASS', test.expected_message))

    def addFailure(self, test, err):
        super(TestResultTable, self).addFailure(test, err)
        self.test_results.append((test, 'FAIL', test.expected_message))

    def addError(self, test, err):
        super(TestResultTable, self).addError(test, err)
        self.test_results.append((test, 'ERROR', test.expected_message))

    def addSkip(self, test, reason):
        super(TestResultTable, self).addSkip(test, reason)
        self.test_results.append((test, 'SKIP', test.expected_message))

    def print_results(self):
        print("\nTest Results Summary:")
        print(f"{'Test Name':<40} {'Result':<10} {'Expected Message'}")
        print("="*70)
        for test, result, message in self.test_results:
            test_name = test.id().split('.')[-1]
            print(f"{test_name:<40} {result:<10} {message}")


class TestRunnerWithTable(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        super(TestRunnerWithTable, self).__init__(*args, **kwargs)
        self.resultclass = TestResultTable

    def run(self, test):
        result = super(TestRunnerWithTable, self).run(test)
        result.print_results()
        return result

      
if __name__ == "__main__":
    unittest.main(testRunner=TestRunnerWithTable())
