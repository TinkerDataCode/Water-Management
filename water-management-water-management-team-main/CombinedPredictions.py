import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta

def combine_predictions(DateofPrediction):
    combined_results = {}
    # Initialize an empty list to store the dates
    date_list = ["Parameter"]
    start_date = datetime.strptime(DateofPrediction, '%Y-%m-%d')

    # Generate the next 5 days and append them to the list
    for _ in range(5):
        date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)

    def predict_and_store(model_file, target_key):
        model = load_model(model_file)
        new_data = pd.read_excel('D:/Case_study/CaseStudy_app/TestingData_Final.xlsx')

        # Specify the DateofPrediction you want to match
        # DateofPrediction = '2023-09-21'

        # Convert 'Date_Sample' column to datetime if it's not already
        new_data['Date_Sample'] = pd.to_datetime(new_data['Date_Sample'])

        # Filter rows where 'Date_Sample' matches DateofPrediction
        matching_data = new_data[new_data['Date_Sample'] == DateofPrediction]
        index_of_matching_data = matching_data[['Temp', 'Rain']].index

        # Extract the integer index
        integer_index = index_of_matching_data[0]

        # Extract the relevant features for prediction (Rain and Temp in this case)
        X_new = new_data[['Rain', 'Temp']].values

        # Scale the input data using separate scalers for each feature
        scaler_rain = MinMaxScaler(feature_range=(0, 1))
        scaler_temp = MinMaxScaler(feature_range=(0, 1))

        # Fit the scalers with their respective features
        scaler_rain.fit(X_new[:, 0].reshape(-1, 1))
        scaler_temp.fit(X_new[:, 1].reshape(-1, 1))

        # Transform each feature separately
        X_new_scaled = np.hstack((scaler_rain.transform(X_new[:, 0].reshape(-1, 1)), scaler_temp.transform(X_new[:, 1].reshape(-1, 1))))

        # Create a window for the input data
        def create_window(data, window_size):
            X = []
            for i in range(window_size, len(data)):
                X.append(data[i - window_size:i, :])
            return np.array(X)

        # Define the window size (should match the size used during training)
        window_size = 4

        # Create windows for the input data
        X_new_windowed = create_window(X_new_scaled, window_size)

        # Predict values for the new data
        predicted_scaled = model.predict(X_new_windowed)

        # Inverse transform the scaled predictions to get the original values
        predicted_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_scaled, X_new_scaled[window_size:, 1:]), axis=1))

        result = []
        for i, value in enumerate(predicted_original_scale):
            print(f'Data Point {i + 1}: Predicted {target_key} = {value[0]}')
            if i >= integer_index and i <= integer_index + 4:
                result.append(value[0])
                print(f'Data Point {i + 1}:')

        combined_results[target_key] = result

    def waterqualityindex():
        weights = {'NO3N': 0.10,'O2Dist': 0.15,'pH': 0.20,'SO4': 0.10,'TN': 0.25,'TP': 0.20}
        wqi_values = []
        wqi_lst  = []
        # Iterate through each set of parameter values
        for i in range(len(combined_results['NO3N'])):
            wqi = 0
            for parameter, value in combined_results.items():
                wqi += (value[i] / max(value)) * weights[parameter]
            wqi_values.append(wqi)
            if wqi > 0.85:
                wqi_lst.append("Excellent")
            elif wqi > 0.70 and wqi <= 0.85:
                wqi_lst.append("Good")
            elif wqi > 0.50 and wqi <= 0.70:
                wqi_lst.append("Fair")
            elif wqi > 0.25 and wqi <= 0.50:
                wqi_lst.append("Poor")
            else:
                wqi_lst.append("Very Poor")

        print(wqi_values)
        combined_results["waterquality_Index"] = wqi_values
        combined_results["waterquality"] = wqi_lst

    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulityNO3.h5', 'NO3N')
    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulityO2-Dis.h5', 'O2Dist')
    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulitypH.h5', 'pH')
    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulitySO4-Tot.h5', 'SO4')
    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulityTN.h5', 'TN')
    predict_and_store('D:/Case_study/CaseStudy_app/19Sep2023/19Sep2023/WaterQulityTP.h5', 'TP')
    waterqualityindex()
    return combined_results, date_list

DateofPrediction = '2023-09-20'
combined_result, date_list = combine_predictions(DateofPrediction)
print(combined_result, date_list)
