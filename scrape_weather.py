"""
scrape_weather.py

Description: This script will scrape the weather data from Environment Canada.
Author: Phillip Bridgeman
"""

import urllib.request as request
from html.parser import HTMLParser
from datetime import datetime

class WeatherScraper:
    def __init__(self):
        self.url = "https://weather.gc.ca/"