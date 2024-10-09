import pandas as pd
import numpy as np

def correct_column_names(df):
    """Correct the column names by removing trailing spaces."""
    df.columns = df.columns.str.strip()
    return df

def transform_water_quality(water_quality_df):
    # Correcting the column names by removing trailing spaces
    water_quality_df.columns = water_quality_df.columns.str.strip()

    # Performing the pivot table transformation
    try:
        water_quality_pivot = water_quality_df.pivot_table(
            values='Values',
            index=['Station', 'Sample_Date'],
            columns='Parameter_Code',
            aggfunc=np.sum
        )
        transform_success = True
    except Exception as e:
        transform_success = False
        error_message = str(e)
        print("Error in pivot transformation:", error_message)
        return None

    water_quality_transformed = water_quality_pivot.reset_index()

    selected_columns = ['Station', 'Sample_Date', 'O2-Dis', 'TEMP', 'pH', 'Month', 'NH4N', 'NO2N', 'TP', 'TOC', 'SO4-Tot', 'TN', 'NO3N', 'Cl-Tot', 'Year', 'Cl-Dis']
    columns_to_drop = [col for col in water_quality_transformed.columns if col not in selected_columns]
    water_quality_transformed = water_quality_transformed.drop(columns=columns_to_drop)
    water_quality_transformed['Station_Date'] = water_quality_transformed['Station'] + ' - ' + water_quality_transformed['Sample_Date'].dt.strftime('%Y-%m-%d')

    return water_quality_transformed

def transform_weather_data(weather_data):
    """Perform the specified transformations on the weather_data DataFrame."""
    
    # Rename columns and format date
    weather_data.rename(columns={'time': 'date'}, inplace=True)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    weather_data['Station_Date'] = weather_data['StationCode'] + ' - ' + weather_data['date'].dt.strftime('%Y-%m-%d')
    
    # Filtering columns
    selected_columns = ['prcp', 'Station_Date']
    weather_data_transformed = weather_data[selected_columns]
    
    return weather_data_transformed

def merge_datasets(water_quality, weather_data, on_column, how='left'):
    """Merge the water quality data with the weather data on a specified column."""
    return water_quality.merge(weather_data, on=on_column, how=how)

def rearrange_and_fill_missing(df, column_order, fill_value=0.0001):
    """Rearrange columns based on the specified order and fill missing values."""
    df = df[column_order]
    df.fillna(fill_value, inplace=True)
    return df