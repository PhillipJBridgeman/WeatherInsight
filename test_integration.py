import unittest
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from unittest.mock import patch, MagicMock

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.scraper = WeatherScraper()
        self.db_ops = DBOperations(":memory:")
        self.db_ops.initialize_db()

    @patch("urllib.request.urlopen")
    def test_scraper_and_db(self, mock_urlopen):
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
                <tr>
                    <th>2024-11-02</th>
                    <td>9.6</td>
                    <td>-4.5</td>
                    <td>2.5</td>
                </tr>
            </tbody>
        </table>
        """
        mock_response = MagicMock()
        mock_response.read.return_value = mock_html.encode("utf-8")
        mock_urlopen.return_value = mock_response

        # Simulate scraping and saving to DB
        url = "http://example.com"
        self.scraper.fetch_data(url)
        self.db_ops.save_data(self.scraper.data)

        # Verify data in DB
        rows = self.db_ops.fetch_data()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("2024-11-01", "Winnipeg", -0.3, 8.0, 3.9))
        self.assertEqual(rows[1], ("2024-11-02", "Winnipeg", -4.5, 9.6, 2.5))
