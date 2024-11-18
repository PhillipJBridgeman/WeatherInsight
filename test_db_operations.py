import unittest
from db_operations import DBOperations

class TestDBOperations(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing
        self.db_ops = DBOperations(":memory:")
        self.db_ops.initialize_db()

    def test_save_and_fetch_data(self):
        # Mock weather data
        weather_data = {
            "2024-11-01": {"Max": 8.0, "Min": -0.3, "Mean": 3.9},
            "2024-11-02": {"Max": 9.6, "Min": -4.5, "Mean": 2.5},
        }

        # Save data
        self.db_ops.save_data(weather_data)

        # Fetch data and verify
        rows = self.db_ops.fetch_data()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ("2024-11-01", "Winnipeg", -0.3, 8.0, 3.9))

    def test_purge_data(self):
        # Mock weather data
        weather_data = {
            "2024-11-01": {"Max": 8.0, "Min": -0.3, "Mean": 3.9},
        }

        # Save and purge data
        self.db_ops.save_data(weather_data)
        self.db_ops.purge_data()

        # Fetch data and verify
        rows = self.db_ops.fetch_data()
        self.assertEqual(len(rows), 0)
