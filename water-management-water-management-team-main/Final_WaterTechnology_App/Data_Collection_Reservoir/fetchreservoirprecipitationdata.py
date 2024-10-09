from datetime import datetime
import pandas as pd
from meteostat import Point, Daily, Stations

# Define a list of station data
station_data = [
    {'GEMS Station Number': 'DEU01634', 'Latitude': 51.19585508, 'Longitude': 9.053268876},
    {'GEMS Station Number': 'DEU01656', 'Latitude': 50.49631157, 'Longitude': 6.421196501},
    {'GEMS Station Number': 'DEU01625', 'Latitude': 49.12643184, 'Longitude': 10.95642},
    {'GEMS Station Number': 'DEU01663', 'Latitude': 51.72761, 'Longitude': 10.85613},
    {'GEMS Station Number': 'DEU01662', 'Latitude': 51.73846, 'Longitude': 10.89115},
    {'GEMS Station Number': 'DEU01654', 'Latitude': 51.65643, 'Longitude': 12.37101},
    {'GEMS Station Number': 'DEU01620', 'Latitude': 50.52318193, 'Longitude': 11.71252999},
    {'GEMS Station Number': 'DEU01642', 'Latitude': 50.61377403, 'Longitude': 11.49425879},
    {'GEMS Station Number': 'DEU01653', 'Latitude': 51.63211, 'Longitude': 12.41256},
    {'GEMS Station Number': 'DEU01680', 'Latitude': 51.34838808, 'Longitude': 7.964561241}
]

def fetch_daily_data(station_data):
    all_data = []

    for station_info in station_data:
        # Fetch station information
        station = Stations().nearby(station_info['Latitude'], station_info['Longitude']).fetch(1)
        station_index = station.index[0]

        # Define start and end dates for daily data
        start = datetime(2008, 1, 1)
        end = datetime(2022, 12, 31)

        # Fetch daily data
        data = Daily(station_index, start, end)
        data = data.fetch()

        # Check if 'time' index is available in the data
        if 'time' in data.index.names:
            # Add 'Station Number' as a new column
            data['Station Number'] = station_info['GEMS Station Number']

            # Append data to the list
            all_data.append(data)
        else:
            print(f"'time' index not found in data for station {station_info['GEMS Station Number']}")

    if all_data:
        # Combine data for all stations
        combined_data = pd.concat(all_data)

        # Reset the index to make 'time' a column
        combined_data.reset_index(inplace=True)

        # Extract 'Station Number', 'time', and 'prcp' columns
        #final_data = combined_data[['Station Number', 'time', 'prcp']]

        # Save final data to a CSV file
        final_csv_file_path = 'weather_final_data_daily1.csv'
        combined_data.to_csv(final_csv_file_path, index=False)

        print(f'Final daily data saved to {final_csv_file_path}')

# Call the function to fetch and combine daily data for all stations
fetch_daily_data(station_data)
