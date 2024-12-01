from scrape_weather import scrape_weather_data
from db_operations import DBOperations
from plot_operations import PlotOperations


def main():
    print("Starting weather data scraping...")
    # Scrape weather data for the range of years 2020 to 2024 and StationID 27174
    weather_data = scrape_weather_data(start_year=2020, end_year=2024, station_id=27174, debug=False)
    print(f"Scraping completed. Sample data: {list(weather_data.items())[:2]}")

    db_ops = DBOperations()
    db_ops.initialize_db()

    print("\nSaving weather data to the database...")
    db_ops.save_data(weather_data)
    print("Data saved successfully!")

    print("\nFetching all raw data from the database...")
    all_data = db_ops.fetch_all_data()
    if all_data:
        print("Raw data fetched (first 5 records):")
        for record in all_data[:5]:
            print(record)
    else:
        print("No data found in the database.")

    print("\nGenerating Box Plot for the year range 2020 to 2024...")
    boxplot_data = db_ops.fetch_data(filter_type="boxplot", year_range=(2020, 2024))
    if boxplot_data:
        plot_ops = PlotOperations()
        plot_ops.generate_boxplot(boxplot_data, year_range=(2020, 2024))
        print("Box Plot generated successfully!")
    else:
        print("No data available for Box Plot generation.")

    print("\nGenerating Line Plot for January 2020...")
    lineplot_data = db_ops.fetch_data(filter_type="lineplot", year=2020, month=1)
    if lineplot_data:
        plot_ops.generate_lineplot(lineplot_data, year=2020, month=1)
        print("Line Plot generated successfully!")
    else:
        print("No data available for Line Plot generation.")

    print("\nDo you want to purge all data from the database? (yes/no): ", end="")
    choice = input().strip().lower()
    if choice == "yes":
        db_ops.purge_data()
        print("Database purged successfully.")
    else:
        print("Purge operation canceled.")


if __name__ == "__main__":
    main()
