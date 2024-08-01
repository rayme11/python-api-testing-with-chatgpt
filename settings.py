import os

# Retrieve the API key from environment variables
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Define the API endpoint
URL = "https://api.openweathermap.org/data/2.5/weather"