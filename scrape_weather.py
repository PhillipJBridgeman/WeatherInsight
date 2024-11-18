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
                    return None
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
        end_date = datetime(1996, 10, 1)
        weather_data = {}

        urls = []
        current_date = start_date
        while current_date >= end_date:
            year, month = current_date.year, current_date.month
            url = (
                f"{base_url}?StationID={station_id}"
                f"&timeframe=2&StartYear=1840&EndYear={year}"
                f"&Day=1&Year={year}&Month={month}"
            )
            urls.append((url, current_date.strftime("%Y-%m")))
            if month == 1:
                current_date = datetime(year - 1, 12, 1)
            else:
                current_date = datetime(year, month - 1, 1)

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_date = {executor.submit(self.fetch_data, url): date for url, date in urls}

            for future in as_completed(future_to_date):
                date = future_to_date[future]
                try:
                    result = future.result()
                    if result:
                        weather_data.update(result)
                except (urllib.error.HTTPError, urllib.error.URLError) as e:
                    print(f"Error processing data for {date}: {e}")
                except ValueError as e:
                    print(f"Value error processing data for {date}: {e}")
        return weather_data
