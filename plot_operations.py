'''
plot_operations.py

Description: Handles all plotting operations for the weather application.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: December 1, 2024
Version: 1.2
Copyright: (c) 2024 Phillip Bridgeman
'''
from collections import defaultdict
import matplotlib.pyplot as plt

class PlotOperations:
    '''
    PlotOperations class to handle all plotting operations.
    '''
    def __init__(self):
        '''
        Initialize the PlotOperations class.
        '''
        self.figsize = (10, 6)
        self.grid = True

    def prepare_boxplot_data(self, raw_data):
        """
        Prepares data for a box plot from the raw database records.
        :param raw_data: List of tuples (e.g., [('01', -7.9), ('02', -7.1), ...])
        :return: Dictionary where keys are months (1-12) and values are lists of mean temperatures.
        """
        data = defaultdict(list)
        for record in raw_data:
            month = int(record[0])  # Convert '01', '02', etc. to integers
            data[month].append(record[1])  # Add mean temp to the respective month
        return data

    def prepare_lineplot_data(self, raw_data):
        """
        Prepares data for a line plot from the raw database records.
        :param raw_data: List of tuples (e.g., [('01', -7.9), ('02', -7.1), ...])
        :return: Two lists: days and mean temperatures.
        """
        days = [int(record[0]) for record in raw_data]
        temps = [record[1] for record in raw_data]
        return days, temps

    def generate_boxplot(self, raw_data, year_range):
        """
        Generate a boxplot for mean temperatures grouped by month.

        :param raw_data: List of tuples fetched from the database (month, mean_temp).
        :param year_range: Tuple indicating the start and end years.
        """
        # Prepare data using helper method
        month_data = self.prepare_boxplot_data(raw_data)

        # Convert dictionary values to lists for plotting
        sorted_months = sorted(month_data.keys())  # Ensure months are in order
        plot_data = [month_data[month] for month in sorted_months]

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.boxplot(plot_data, labels=[str(month) for month in sorted_months])
        plt.title(f"Monthly Temperature Distribution for {year_range[0]} to {year_range[1]}")
        plt.xlabel("Month")
        plt.ylabel("Mean Temperature (°C)")
        plt.grid(True)
        plt.show()

    def generate_lineplot(self, raw_data, year, month):
        """
        Generates a line plot for daily mean temperatures in a specific month and year.
        :param raw_data: List of tuples (e.g., [(1, -7.9), (2, -7.1), ...]).
        :param year: Year of the data.
        :param month: Month of the data (1-12).
        """
        days, temps = self.prepare_lineplot_data(raw_data)
        plt.figure(figsize=(10, 6))
        plt.plot(days, temps, marker='o', linestyle='-')
        plt.title(f"Daily Mean Temperatures for {year}-{month:02d}")
        plt.xlabel("Day")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.show()
