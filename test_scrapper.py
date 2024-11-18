import unittest
from unittest.mock import patch, MagicMock
from scrape_weather import WeatherScraper

class TestWeatherScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WeatherScraper()

    @patch("urllib.request.urlopen")
    def test_scrape_valid_html(self, mock_urlopen):
        # Mock HTML response
        mock_html = """
        <table class="data-table">
            <tbody>
                <tr>
                    <th>2024-11-01</th>
                    <td>8.0</td>
                    <td>-0.3</td>
                    <td>3.9</td>
                </tr>
            </tbody>
        </table>
        """
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html.encode("utf-8")
        mock_urlopen.return_value = mock_response

        # Call scraper
        url = "http://example.com"
        self.scraper.fetch_data(url)

        # Debugging prints
        print(f"Scraped data: {self.scraper.data}")

        # Assert that data was scraped correctly
        self.assertIn("2024-11-01", self.scraper.data)
        self.assertEqual(self.scraper.data["2024-11-01"], {"Max": 8.0, "Min": -0.3, "Mean": 3.9})
