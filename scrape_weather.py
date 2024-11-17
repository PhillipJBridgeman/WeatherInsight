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

# Fetch HTML content
base_url = "http://climate.weather.gc.ca/climate_data/daily_data_e.html"
station_id = 27174 # Winnipeg Station ID
year = 2024
month = 11

url = f"{base_url}?StationID={station_id}&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}"
with urllib.request.urlopen(url) as response:
    html_content = response.read().decode("utf-8")

# Scrape data
scraper = WeatherScraper()
scraper.feed(html_content)

# Print the scraped data
for date, temps in scraper.data.items():
    print(
        f"Date: {date}, "
        f"Max Temp: {temps['Max Temp']}, "
        f"Min Temp: {temps['Min Temp']}, "
        f"Mean Temp: {temps['Mean Temp']}"
    )
