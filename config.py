import os
import requests
from settings import API_KEY, URL


def setup():
    # Ensure the API key is available
    if API_KEY is None:
        raise ValueError(
            "API key for OpenWeatherMap is not set. Please set the OPENWEATHERMAP_API_KEY environment variable.")

   
    # Define the parameters for the API request
    params = {
        "q": "London",  # The city to query
        "appid": API_KEY  # The API key
    }

   
    try:
        # Make the API request
        response = requests.get(URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            print("Connection and first test was ok !!")
            weather_data = response.json()
            # print(weather_data)
    except ConnectionError as e:
        raise ConnectionError(f"Failed to connect to API: {e}")
    


if __name__ == "__main__":
    setup()