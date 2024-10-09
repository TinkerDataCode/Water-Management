import pandas as pd

def load_water_quality_data_from_excel(file_path, sheet_name='Water-Quality '):
    """Load the water quality data from an Excel file."""
    try:
        water_quality = pd.read_excel(file_path, sheet_name=sheet_name)
        return water_quality, None
    except Exception as e:
        return None, str(e)

def load_weather_data_from_csv(file_path):
    """Load the weather data from a CSV file."""
    try:
        weather_data = pd.read_csv(file_path)
        return weather_data, None
    except Exception as e:
        return None, str(e)
