from datetime import datetime, timedelta
from meteostat import Point, Daily
import pandas as pd
import sys
import os
#sys.path.append("D:/Case_study/CaseStudy_app/new_file/new_file")

script_dir = os.path.dirname(__file__)


def fetch_recent_weather_data():
    start = datetime(2023, 9, 19)
    end = start + timedelta(days=10)  # Adjust the number of days as needed

    # Create Point for Neckar river Mannheim
    location = Point(49.49468873, 8.46889864)

    # Fetch the data
    data = Daily(location, start, end)
    data = data.fetch()
    relative_file_path_1 = 'recent_data.csv'
    file_path_1 = os.path.join(script_dir, relative_file_path_1)
    data.to_csv(file_path_1, mode='w')

    df = pd.read_csv(file_path_1)

    # Extract 'time' and 'prcp' columns
    recent_weather_data = df[['time', 'prcp']]

    # Replace NaN values in 'prcp' with 0
    recent_weather_data['prcp'].fillna(0, inplace=True)
    relative_file_path_2 = 'recent_weather_data.csv'
    file_path_2 = os.path.join(script_dir, relative_file_path_2)
    # Save the cleaned data to a new CSV file
    recent_weather_data.to_csv(file_path_2, mode='w',
                               index=False)

    return recent_weather_data


# Call the function to execute the code
fetch_recent_weather_data()
