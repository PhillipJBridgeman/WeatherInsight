'''
weather_processor.py
Description: Main script to handle user interactions for managing and visualizing weather data.
Author: Phillip Bridgeman
Date: December 1, 2024
Last Modified: December 1, 2024
Version: 1.0
Copyright: (c) 2024 Phillip Bridgeman
'''
import tkinter as tk
from datetime import datetime, date
from tkinter import messagebox
from tkinter import ttk
from scrape_weather import scrape_weather_data
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """
    WeatherProcessor class handles all user interactions for managing and visualizing weather data.
    """
    def __init__(self, main_root):
        """Initialize the WeatherProcessor class."""
        self.root = main_root
        self.db_ops = DBOperations()
        self.plot_ops = PlotOperations()

        # Create a frame for the main application
        self.frame = tk.Frame(main_root)
        self.frame.pack(fill="both", expand=True)

        # Add buttons for menu options
        tk.Button(self.frame, text="Download Full Data", command=self.download_data).pack(pady=10)
        tk.Button(self.frame, text="Update Data", command=self.update_data).pack(pady=10)
        tk.Button(self.frame, text="Generate Box Plot", 
                  command=self.generate_box_plot_gui).pack(pady=10)
        tk.Button(self.frame, text="Generate Line Plot", 
                  command=self.generate_line_plot_gui).pack(pady=10)
        tk.Button(self.frame, text="Exit", command=self.root.quit).pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.frame, text="Status: Ready")
        self.status_label.pack(pady=10)

    def download_data(self):
        """Download the full weather dataset for a predefined range of years."""
        self.status_label.config(text="Status: Downloading full data...")
        current_year = date.today().year
        weather_data = scrape_weather_data(start_year=2020,
                                           end_year=current_year,
                                           station_id=27174,
                                           debug=False)
        self.db_ops.save_data(weather_data)
        self.status_label.config(text="Status: Data downloaded successfully!")

    def update_data(self):
        """
        Update the weather data by fetching data from the latest date in the database to today.
        """
        self.status_label.config(text="Status: Updating data...")
        last_date = self.db_ops.get_latest_date()

        if not last_date:
            self.status_label.config(text=(
                "Status: No data found. Please download the full dataset first."
                ))
            return

        last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
        current_date = date.today()

        if last_date >= current_date:
            self.status_label.config(text="Status: Weather data is already up to date.")
            return

        weather_data = scrape_weather_data(
            start_year=last_date.year, end_year=current_date.year, station_id=27174, debug=False
        )
        self.db_ops.save_data(weather_data)
        self.status_label.config(text="Status: Data updated successfully!")

    def generate_box_plot_gui(self):
        """Display input fields for the year range and generate a box plot."""
        # Create a new window for user input
        input_window = tk.Toplevel(self.frame)
        input_window.title("Box Plot Input")

        # Input fields
        tk.Label(input_window, text="Start Year:").pack(pady=5)
        start_year_entry = tk.Entry(input_window)
        start_year_entry.pack(pady=5)

        tk.Label(input_window, text="End Year:").pack(pady=5)
        end_year_entry = tk.Entry(input_window)
        end_year_entry.pack(pady=5)

        def submit():
            start_year = start_year_entry.get().strip()
            end_year = end_year_entry.get().strip()
            self.generate_box_plot(start_year, end_year)
            input_window.destroy()

        tk.Button(input_window, text="Submit", command=submit).pack(pady=10)

    def generate_box_plot(self, start_year, end_year):
        """Generate a box plot for a specified year range."""
        self.status_label.config(text="Status: Generating box plot...")
        boxplot_data = self.db_ops.fetch_data(filter_type="boxplot",
                                              year_range=(start_year, end_year))
        if boxplot_data:
            self.plot_ops.generate_boxplot(boxplot_data, year_range=(start_year, end_year))
            self.status_label.config(text="Status: Box plot generated successfully!")
        else:
            self.status_label.config(text="Status: No data available for the selected year range.")

    def generate_line_plot_gui(self):
        """GUI for generating a line plot."""
        def submit():
            year = year_entry.get().strip()
            month = month_var.get().strip()
            if not year.isdigit() or not month.isdigit():
                messagebox.showerror("Input Error", "Year and Month must be numeric.")
                return
            try:
                self.generate_line_plot(year, month)
                plot_window.destroy()
            except (TypeError, RuntimeError) as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        plot_window = tk.Toplevel(self.root)  # Use `self.root` as the parent
        plot_window.title("Generate Line Plot")
        plot_window.geometry("400x200")

        tk.Label(plot_window, text="Year:").pack(pady=5)
        year_entry = tk.Entry(plot_window)
        year_entry.pack(pady=5)

        tk.Label(plot_window, text="Month:").pack(pady=5)
        month_var = tk.StringVar()
        month_dropdown = ttk.Combobox(
            plot_window,
            textvariable=month_var,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
        )
        month_dropdown.set("1")  # Set default value to January
        month_dropdown.pack(pady=5)

        tk.Button(plot_window, text="Generate", command=submit).pack(pady=10)

    def generate_line_plot(self, year, month):
        """Generate a line plot for a specified month and year."""
        try:
            # Convert month to an integer for formatting
            month = int(month)

            self.status_label.config(text="Status: Generating line plot...")
            lineplot_data = self.db_ops.fetch_data(filter_type="lineplot", year=year, month=month)
            if lineplot_data:
                self.plot_ops.generate_lineplot(lineplot_data, year=year, month=month)
                self.status_label.config(text="Status: Line plot generated successfully!")
            else:
                self.status_label.config(
                    text="Status: No data available for the selected month and year."
                )
        except ValueError:
            self.status_label.config(text="Input Error: Year and Month must be valid numbers.")
            messagebox.showerror("Input Error", "Year and Month must be valid numbers.")
        except (TypeError, RuntimeError) as e:
            self.status_label.config(text=f"Error: {e}")
            messagebox.showerror("Error", f"Failed to generate line plot: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Weather Insight")
    app = WeatherProcessor(root)
    root.mainloop()
