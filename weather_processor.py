'''
weather_processor.py
Description: Main script to handle user interactions for managing and visualizing weather data.
Author: Phillip Bridgeman
Date: Decemebr 1, 2024
Last Modified: December 1, 2024
Version: 1.0
Copyright: (c) 2024 Phillip Bridgeman
'''
from datetime import datetime, date
from scrape_weather import scrape_weather_data
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """
    WeatherProcessor class handles all user interactions for managing and visualizing weather data.
    """
    def __init__(self):
        '''
        Initialize the WeatherProcessor class.
        '''
        self.db_ops = DBOperations()
        self.plot_ops = PlotOperations()

    def display_menu(self):
        """
        Display the main menu and handle user input for different tasks.
        """
        while True:
            print("\nWeather Processor")
            print("1. Download full weather data")
            print("2. Update weather data")
            print("3. Generate box plot (year range)")
            print("4. Generate line plot (month and year)")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.download_data()
            elif choice == "2":
                self.update_data()
            elif choice == "3":
                self.generate_box_plot()
            elif choice == "4":
                self.generate_line_plot()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def download_data(self):
        """
        Download the full weather dataset for a predefined range of years.
        """
        print("Starting download of full weather data...")
        current_year = date.today().year  # Dynamically get the current year
        weather_data = scrape_weather_data(
            start_year=2020, end_year=current_year, station_id=27174, debug=False
        )
        print("Scraping completed. Saving data to the database...")
        self.db_ops.save_data(weather_data)
        print("Data downloaded and saved successfully!")

    def update_data(self):
        """
        Update the weather data by fetching data from the latest date in the database to today.
        """
        print("Updating weather data...")
        last_date = self.db_ops.get_latest_date()

        if not last_date:
            print("No data found. Please download the full dataset first.")
            return

        last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        current_date = date.today()

        if last_date >= current_date:
            print("Weather data is already up to date.")
            return

        print(f"Fetching data from {last_date} to {current_date}...")
        weather_data = scrape_weather_data(
            start_year=last_date.year, end_year=current_date.year, station_id=27174, debug=False
        )
        self.db_ops.save_data(weather_data)
        print("Weather data updated successfully!")

    def generate_box_plot(self):
        """
        Generate a box plot for a specified year range.
        """
        print("\nEnter the year range for the box plot:")
        try:
            start_year = int(input("Start year: ").strip())
            end_year = int(input("End year: ").strip())
        except ValueError:
            print("Invalid input. Please enter valid years.")
            return

        boxplot_data = self.db_ops.fetch_data(filter_type="boxplot", year_range=(start_year, end_year))
        if boxplot_data:
            print(f"Generating box plot for the range {start_year}–{end_year}...")
            self.plot_ops.generate_boxplot(boxplot_data, year_range=(start_year, end_year))
            print("Box plot generated successfully!")
        else:
            print("No data available for the selected range.")

    def generate_line_plot(self):
        """
        Generate a line plot for a specified month and year.
        """
        print("\nEnter the month and year for the line plot:")
        try:
            year = int(input("Year: ").strip())
            month = int(input("Month (1–12): ").strip())
            if month < 1 or month > 12:
                print("Invalid month. Please enter a value between 1 and 12.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid year and month.")
            return

        lineplot_data = self.db_ops.fetch_data(filter_type="lineplot", year=year, month=month)
        if lineplot_data:
            print(f"Generating line plot for {month}/{year}...")
            self.plot_ops.generate_lineplot(lineplot_data, year=year, month=month)
            print("Line plot generated successfully!")
        else:
            print("No data available for the selected month and year.")


if __name__ == "__main__":
    processor = WeatherProcessor()
    processor.display_menu()
