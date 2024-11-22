"""
scrape_weather.py

Description: This script will scrape the weather data from Environment Canada.
Author: Phillip Bridgeman
Date: October 30, 2024
Last Modified: November 17, 2024
Version: 1.0
"""

import urllib.request
from html.parser import HTMLParser
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class WeatherScraper(HTMLParser):
    '''
    WeatherScraper class to extract weather data from the HTML content.
    '''
    def __init__(self):
        '''
        Initialize the WeatherScraper object.
        '''
        super().__init__()
        self.in_table = False
        self.in_tbody = False
        self.current_row = []
        self.headers = []
        self.data = {}
        self.current_date = None

    def handle_starttag(self, tag, attrs):
        '''
        Handle the start tag of an HTML element.
        '''
        attrs = dict(attrs)
        if tag == "table" and "class" in attrs and "data-table" in attrs["class"]:
            self.in_table = True
        elif self.in_table and tag == "tbody":
            self.in_tbody = True
        elif self.in_tbody and tag == "th":
            self.current_row = []

    def handle_endtag(self, tag):
        '''
        Handle the end tag of an HTML element.
        '''
        if tag == "table" and self.in_table:
            self.in_table = False
        elif tag == "tbody" and self.in_tbody:
            self.in_tbody = False
        elif tag == "tr" and self.in_tbody:
            if len(self.current_row) >= 3 and self.current_date not in ["Sum", "Avg", "Xtrm"]:
                self.data[self.current_date] = {
                    "Max Temp": self.current_row[0],
                    "Min Temp": self.current_row[1],
                    "Mean Temp": self.current_row[2]
                }
            elif self.current_date in ["Sum", "Avg", "Xtrm"]:
                print(f"Skipping summary row: {self.current_date}")

            self.current_row = []
            self.current_date = None

    def handle_data(self, data):
        '''
        Handle the data within an HTML element.
        '''
        if self.in_tbody:
            if data.strip():
                if len(self.current_row) == 0 and self.current_date is None:
                    self.current_date = data.strip()
                else:
                    try:
                        self.current_row.append(float(data.strip()))
                    except ValueError:
                        self.current_row.append(None)

    def fetch_data(self, url):
        '''
        Fetch the weather data from the specified URL.
        '''
        try:
            with urllib.request.urlopen(url) as response:
                html_content = response.read().decode("utf-8")
                if "No data available for this station" in html_content:
                    return None  # Stop if no data available
                self.feed(html_content)
                return self.data.copy()
        except urllib.error.HTTPError as e:
            print(f"Error fetching data from {url}: {e}")
            return None
        except urllib.error.URLError as e:
            print(f"HTTP error fetching data from {url}: {e}")
            return None

    def scrape(self, base_url, station_id):
        '''
        Scrape the weather data from the specified base URL and station ID.
        '''
        start_date = datetime.now()
        weather_data = {}
        current_date = start_date

        while True:
            year, month = current_date.year, current_date.month
            url = (
                f"{base_url}?StationID={station_id}"
                f"&timeframe=2&StartYear=1840&EndYear={year}"
                f"&Day=1&Year={year}&Month={month}"
            )
            print(f"Fetching data for {current_date.strftime('%Y-%m')}...")
            result = self.fetch_data(url)
            if not result:  # Stop if no data is available
                print("No more data available. Stopping.")
                break
            weather_data.update(result)

            # Go to the previous month
            if month == 1:
                current_date = datetime(year - 1, 12, 1)
            else:
                current_date = datetime(year, month - 1, 1)

        return weather_data


if __name__ == "__main__":
    base_url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html"
    station_id = 27174  # Example: Winnipeg Station ID
    
    scraper = WeatherScraper()
    print("Starting weather data scraping...")
    weather_data = scraper.scrape(base_url, station_id)
    
    if weather_data:
        print("Scraping completed successfully! Here is some sample data:\n")
        for date, data in list(weather_data.items())[:5]:  # Display first 5 entries
            print(f"{date}: Max: {data['Max Temp']}, Min: {data['Min Temp']}, Mean: {data['Mean Temp']}")
    else:
        print("No data was scraped.")
