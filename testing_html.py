import urllib.request
from datetime import datetime

# Define the base URL and parameters
base_url = "http://climate.weather.gc.ca/climate_data/daily_data_e.html"
station_id = 27174  # Winnipeg Station ID
year = datetime.now().year
month = datetime.now().month

# Construct the URL for the current month
url = f"{base_url}?StationID={station_id}&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}"

try:
    # Fetch the HTML content
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    
    # Print the HTML content to understand the structure
    print(html)
except Exception as e:
    print(f"Error fetching HTML content: {e}")