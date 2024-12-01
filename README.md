# WeatherInsight
WeatherInsight is a Python-based application that allows users to scrape, manage, and visualize weather data for specified date ranges. The application features a menu-driven interface to facilitate easy interaction.
---
## Features
- **Download Weather Data:** Fetch a complete dataset for a predefined range of years.
- **Update Weather Data:** Update the database with missing weather data, ensuring no duplication.
- **Visualize Data:**
    - Generate a Box Plot for a specified year range.
    - Generate a Line Plot for a specified month and year.
- **Menu-Driven Interface:** Intuitive and user-friendly navigation.
---
## Getting Started
### Prerequisites
Ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)
- SQLite (for database management)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/PhillipJBridgeman/WeatherInsight.git
cd WeatherInsight
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
# source venv/bin/activate   # On macOS/Linux
```
3. Install required dependencies:
```bash
pip install -r requirements.txt
```
4. Ensure sqlite3 is installed and available in your system PATH:
- Verify by running:
```bash
sqlite3 --version
```
---
## Usage
Run the application by executing weather_processor.py:
```bash
python weather_processor.py
```
## Menu Options
1. Download Weather Data (Full Range):
    - Fetch a complete dataset for the predefined range of years (2020 to the current year).
    - Automatically save the data to the SQLite database.
2. Update Weather Data (Latest to Current):
    - Check the database for the latest available weather data.
    - Fetch and save missing weather data from the last recorded date to today.
3. Visualize Data: Box Plot (Year Range):
    - Enter a start and end year to generate a box plot of average temperatures for the selected range.
4. Visualize Data: Line Plot (Month & Year):
    - Enter a specific month and year to generate a line plot of daily average temperatures for the chosen period.
5. Exit Program:
    - Exit the application.
---
## Project Structure
```graphql
WeatherInsight/
├── dbcm.py                 # Database context manager
├── db_operations.py        # Handles database operations (save, fetch, update)
├── plot_operations.py      # Generates data visualizations (box and line plots)
├── requirements.txt        # Project dependencies
├── scrape_weather.py       # Web scraping logic
├── weather_processor.py    # Main entry point for the application
└── weather_data.db         # SQLite database file (generated on first run)
```
---
## Database Schema
The SQLite database (weather_data.db) contains a single table:
### Table: weather
| Column      | Type 	 | Description                  |
| ----------- | -------- | ---------------------------- |
| id	      | INTEGER	 | Primary key (auto-increment) |
| sample_date |	TEXT	 | Date of the weather record   |
| location    | TEXT	 | Location of the weather data |
| min_temp	  | REAL	 | Minimum temperature (°C)     |
| max_temp    | REAL	 | Maximum temperature (°C)     |
| avg_temp    | REAL     | Average temperature (°C)     |
---
## Example Usage
### Run the Application
```bash
python weather_processor.py
```
1. Select 1 to download the full dataset:
```bash
Enter your choice: 1
Starting download of full weather data...
Scraping completed. Saving data to the database...
Data downloaded and saved successfully!
```
2. Select 2 to update weather data:
```bash
Enter your choice: 2
Updating weather data...
Fetching data from 2024-11-30 to 2024-12-01...
Weather data updated successfully!
```
3. Select 3 to generate a box plot:
```bash
Enter your choice: 3
Enter the year range for the box plot:
Start year: 2020
End year: 2024
Generating box plot for the range 2020–2024...
Box plot generated successfully!
```
4. Select 4 to generate a line plot:
```bash
Enter your choice: 4
Enter the month and year for the line plot:
Year: 2024
Month (1–12): 12
Generating line plot for 12/2024...
Line plot generated successfully!
```
---
## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository
2. Create a new feature branch:
```bash
git checkout -b feature-branch-name
```
3. Commit your changes:
```bash
git commit -m "Add your message here"
```
4. Push to your branch:
```bash
git push origin feature-branch-name
```
5. Open a Pull Request on GitHub.
---
## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Weather data is sourced from Environment Canada.
- Developed as part of the Business Information Technology program at Red River College Polytechnic.