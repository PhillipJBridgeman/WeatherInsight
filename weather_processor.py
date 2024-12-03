"""
weather_processor.py
Description: Combined script for managing and visualizing weather data via a GUI.
Author: Phillip Bridgeman
Date: December 3, 2024
Last Modified: December 3, 2024
Version: 2.0
Copyright: (c) 2024 Phillip Bridgeman
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from scrape_weather import scrape_weather_data
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor:
    """
    WeatherApp class provides a unified interface for managing and visualizing weather data.
    """

    def __init__(self, main_root):
        """Initialize the WeatherApp class."""
        self.root = main_root
        self.db_ops = DBOperations()
        self.plot_ops = PlotOperations()

        self.db_ops.initialize_db()

        self.setup_ui()

    def setup_ui(self):
        """Setup the main GUI layout."""
        self.root.title("Weather Insight")
        self.root.geometry("800x600")
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Button(frame, text="Download Full Data", command=self.download_data).pack(pady=10)
        tk.Button(frame, text="Update Data", command=self.update_data).pack(pady=10)
        tk.Button(frame, text="Generate Box Plot", command=self.generate_box_plot_gui).pack(pady=10)
        tk.Button(frame, text="Generate Line Plot", command=self.generate_line_plot_gui
                  ).pack(pady=10)
        tk.Button(frame, text="Exit", command=self.root.quit).pack(pady=10)

        self.status_label = tk.Label(frame, text="Status: Ready")
        self.status_label.pack(pady=10)

    def download_data(self):
        """Download the full weather dataset for a predefined range of years."""
        try:
            self.status_label.config(text="Status: Downloading data...")
            current_year = date.today().year
            weather_data = scrape_weather_data(start_year=2020,
                                               end_year=current_year,
                                               station_id=27174,
                                               debug=False)
            self.db_ops.save_data(weather_data)
            self.status_label.config(text="Status: Data downloaded successfully!")
            messagebox.showinfo("Success", "Data downloaded and saved successfully!")
        except (ConnectionError, ValueError) as e:
            self.status_label.config(text="Status: Error downloading data.")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_data(self):
        """Update weather data from the latest available date to today."""
        try:
            self.status_label.config(text="Status: Updating data...")
            last_date = self.db_ops.get_latest_date()
            if not last_date:
                self.status_label.config(
                    text="Status: No data found. Please download the full dataset first."
                    )
                messagebox.showwarning("Warning",
                                       "No data found. Please download the full dataset first."
                                       )
                return

            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            current_date = date.today()
            if last_date >= current_date:
                self.status_label.config(text="Status: Data is already up to date.")
                messagebox.showinfo("Info", "Weather data is already up to date.")
                return

            weather_data = scrape_weather_data(start_year=last_date.year,
                                               end_year=current_date.year,
                                               station_id=27174,
                                               debug=False)
            self.db_ops.save_data(weather_data)
            self.status_label.config(text="Status: Data updated successfully!")
            messagebox.showinfo("Success", "Weather data updated successfully!")
        except (ConnectionError, ValueError) as e:
            self.status_label.config(text="Status: Error updating data.")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_box_plot_gui(self):
        """GUI for generating a box plot."""
        def submit():
            start_year = start_year_entry.get().strip()
            end_year = end_year_entry.get().strip()
            try:
                self.generate_box_plot(start_year, end_year)
                plot_window.destroy()
            except (ValueError, TypeError) as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Generate Box Plot")
        plot_window.geometry("400x200")

        tk.Label(plot_window, text="Start Year:").pack(pady=5)
        start_year_entry = tk.Entry(plot_window)
        start_year_entry.pack(pady=5)

        tk.Label(plot_window, text="End Year:").pack(pady=5)
        end_year_entry = tk.Entry(plot_window)
        end_year_entry.pack(pady=5)

        tk.Button(plot_window, text="Generate", command=submit).pack(pady=10)

    def generate_line_plot_gui(self):
        """GUI for generating a line plot."""
        def submit():
            year = year_entry.get().strip()
            month = month_var.get()
            try:
                self.generate_line_plot(year, month)
                plot_window.destroy()
            except (ValueError, TypeError) as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        plot_window = tk.Toplevel(self.root)
        plot_window.title("Generate Line Plot")
        plot_window.geometry("400x200")

        tk.Label(plot_window, text="Year:").pack(pady=5)
        year_entry = tk.Entry(plot_window)
        year_entry.pack(pady=5)

        tk.Label(plot_window, text="Month:").pack(pady=5)
        month_var = tk.StringVar()
        month_dropdown = ttk.Combobox(plot_window,
                                      textvariable=month_var,
                                      values=[str(i) for i in range(1, 13)]
                                      )
        month_dropdown.pack(pady=5)

        tk.Button(plot_window, text="Generate", command=submit).pack(pady=10)

    def generate_box_plot(self, start_year, end_year):
        """Generate a box plot for the specified year range."""
        try:
            self.status_label.config(text="Status: Generating box plot...")
            boxplot_data = self.db_ops.fetch_data(filter_type="boxplot",
                                                  year_range=(start_year, end_year)
                                                  )
            if boxplot_data:
                self.plot_ops.generate_boxplot(boxplot_data, year_range=(start_year, end_year))
                self.status_label.config(text="Status: Box plot generated successfully!")
            else:
                self.status_label.config(text="Status: No data for selected range.")
                messagebox.showinfo("Info", "No data available for the selected year range.")
        except (ValueError, TypeError) as e:
            self.status_label.config(text="Status: Error generating box plot.")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_line_plot(self, year, month):
        """Generate a line plot for the specified month and year."""
        try:
            self.status_label.config(text="Status: Generating line plot...")
            lineplot_data = self.db_ops.fetch_data(filter_type="lineplot", year=year, month=month)
            if lineplot_data:
                self.plot_ops.generate_lineplot(lineplot_data, year=int(year), month=int(month))
                self.status_label.config(text="Status: Line plot generated successfully!")
            else:
                self.status_label.config(text="Status: No data for selected month and year.")
                messagebox.showinfo("Info", "No data available for the selected month and year.")
        except (ValueError, TypeError) as e:
            self.status_label.config(text="Status: Error generating line plot.")
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherProcessor(root)
    root.mainloop()
