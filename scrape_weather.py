'''
scrape_weather.py

Description: A script to scrape weather data from the Government of Canada website.
Author: Phillip Bridgeman
Date: October 30, 2024
Last Modified: November 22, 2024
Version: 1.11
'''

from html.parser import HTMLParser
import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor
from thread_cal import calculate_thread_pool

class WeatherScraper(HTMLParser):
    '''
    WeatherScraper class to scrape weather data from the Government of Canada website.
    '''
    def __init__(self, debug=False):
        '''
        Initialize the WeatherScraper class.
        :param debug: If True, print debug information. Default is False.
        '''
        super().__init__()
        self.current_year = None
        self.current_month = None
        self.current_date = None
        self.current_row = []
        self.weather_data = {}
        self.in_tbody = False
        self.debug = debug

    def handle_starttag(self, tag, attrs):
        '''
        Handle the start tag of an HTML element.
        '''
        if tag == "tbody":
            self.in_tbody = True

    def handle_endtag(self, tag):
        '''
        Handle the end tag of an HTML element.
        '''
        if tag == "tbody":
            self.in_tbody = False

        if tag == "tr" and self.current_date:
            if len(self.current_row) >= 3:
                try:
                    self.weather_data[self.current_date] = {
                        "Max": float(self.current_row[0]) if self.current_row[0] else None,
                        "Min": float(self.current_row[1]) if self.current_row[1] else None,
                        "Mean": float(self.current_row[2]) if self.current_row[2] else None,
                    }
                except ValueError:
                    pass
            self.current_date = None
            self.current_row = []

    def handle_data(self, data):
        '''
        Handle the data within an HTML element.
        '''
        try:
            if self.in_tbody:
                clean_data = data.strip()
                if not self.current_date and clean_data.isdigit():
                    self.current_date = (
                        f"{self.current_year}-{self.current_month:02d}-{int(clean_data):02d}"
                        )
                elif clean_data:
                    self.current_row.append(clean_data)
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as e:
            if self.debug:
                print(f"Error parsing data: {e}")

    def fetch_and_parse(self, year, month, station_id):
        '''
        Fetch and parse the weather data for a given year and month.
        '''
        self.current_year = year
        self.current_month = month
        url = (
            f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
            f"StationID={station_id}&timeframe=2&StartYear=1840&EndYear=2020&Day=1"
            f"&Year={year}&Month={month}"
        )
        if self.debug:
            print(f"Fetching data from: {url}")
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode("utf-8")
                self.feed(content)
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as e:
            if self.debug:
                print(f"Error fetching data from {url}: {e}")


def scrape_weather_data(start_year, end_year, station_id, debug=False):
    '''
    Scrape weather data for a range of years and return it as a dictionary.
    :param debug: If True, print debug information. Default is False.
    '''
    max_threads = calculate_thread_pool(task_type="io")
    if debug:
        print(f"Using {max_threads} threads for scraping.")

    def fetch_for_year_month(year, month):
        scraper = WeatherScraper(debug=debug)
        scraper.fetch_and_parse(year, month, station_id)
        return scraper.weather_data

    all_weather_data = {}

    with ThreadPoolExecutor(max_threads) as executor:
        futures = []
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                futures.append(executor.submit(fetch_for_year_month, year, month))

        for future in futures:
            try:
                weather_data = future.result()
                all_weather_data.update(weather_data)
            except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as e:
                if debug:
                    print(f"Error processing future: {e}")

    return all_weather_data


if __name__ == "__main__":
    # Enable debug mode when running as a standalone script
    scraped_data = scrape_weather_data(start_year=2020, end_year=2024, station_id=27174, debug=True)
    print("Scraping completed. Saving data to file...")
    with open("weather_data_2020_present.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4)
    print("Weather data saved to 'weather_data_2020_present.json'.")
    sample = list(scraped_data.items())[:5]
    print(f"Sample data: {sample}")
