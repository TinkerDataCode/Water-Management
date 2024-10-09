import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import runpy
import sys
import os

script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)

from WQI import calculate_wqi

def river_prediction(date):
    # Load necessary data and models
    relative_file_path_1 = 'recent_weather_data.py'
    file_path_1 = os.path.join(script_dir, relative_file_path_1)
    runpy.run_path(file_path_1)
    
    relative_file_path_2 = 'recent_weather_data.csv'
    file_path_2 = os.path.join(script_dir, relative_file_path_2)
    recent_data = pd.read_csv(file_path_2)
    prcp_values = recent_data['prcp'].values
    time_values = recent_data['time'].values

    model = load_model(script_dir)
    
    relative_file_path_3 = 'scaler_X.pkl'
    file_path_3 = os.path.join(script_dir, relative_file_path_3)
    relative_file_path_4 = 'scaler_y.pkl'
    file_path_4 = os.path.join(script_dir, relative_file_path_4)
    relative_file_path_5 = 'target_cols.pkl'
    file_path_5 = os.path.join(script_dir, relative_file_path_5)
    
    with open(file_path_3, 'rb') as file:
        scaler_X = pickle.load(file)

    with open(file_path_4, 'rb') as file:
        scaler_y = pickle.load(file)

    with open(file_path_5, 'rb') as file:
        target_cols = pickle.load(file)

    # Predict using the trained CNN model and compute WQI for each prediction
    predictions = []
    wqis = []

    prcp_values_list = []  # To store prcp values

    for idx, value in enumerate(prcp_values):
        new_prcp_value = [[value]]
        new_prcp_scaled = scaler_X.transform(new_prcp_value)
        new_prcp_scaled = np.expand_dims(new_prcp_scaled, axis=2)

        # Predict
        predicted_scaled = model.predict(new_prcp_scaled)
        predicted_original = scaler_y.inverse_transform(predicted_scaled)
        predicted_dict = {col: pred for col, pred in zip(target_cols, predicted_original[0])}

        # Calculate WQI for the predicted values
        wqi_value, wqi_category = calculate_wqi(predicted_dict)

        predictions.append(predicted_dict)
        wqis.append((wqi_value, wqi_category))

        # Append the 'prcp' value to the list of 'prcp' values
        prcp_values_list.append(value)

    # Initialize dictionaries to collect the data
    parameter_data = {col: [] for col in target_cols}
    formatted_data = {col: [] for col in target_cols}
    wqi_values = []
    wqi_categories = []
    dates_river = ["Parameter"]

    # Loop through the predictions and collect data
    for idx, (prediction, (wqi_value, wqi_category)) in enumerate(zip(predictions, wqis)):
        date = time_values[idx]
        prcp = prcp_values[idx]

        # Append the date to the list
        dates_river.append(date)

        # Append the 'WQI Value' and 'Category' to their respective lists
        wqi_values.append(wqi_value)
        wqi_categories.append(wqi_category)

        # Append the 'prcp' value to the list of 'prcp' values
        prcp_values_list.append(prcp)

        # Append the predicted values to the respective parameter list
        for col, value in prediction.items():
            parameter_data[col].append(value)

    # Add 'WQI Values' and 'WQI Categories' to the formatted_data dictionary
    formatted_data['WQI Values'] = wqi_values
    formatted_data['WQI Categories'] = wqi_categories

    # Add 'prcp' values to the formatted_data dictionary
    formatted_data['Rain'] = prcp_values_list[:11]

    # Add the parameter data to the formatted_data dictionary
    for col in target_cols:
        formatted_data[col] = parameter_data[col]

    return formatted_data, dates_river

# Call the function to get the results
formatted_data, dates_river = river_prediction("2023-09-20")
print("Formatted Data:")
print(formatted_data)
print("\nDates:")
print(dates_river)
