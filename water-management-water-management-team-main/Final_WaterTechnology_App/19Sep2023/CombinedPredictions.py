import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Load and preprocess the new input data (replace 'new_data.xlsx' with your file path)
new_data = pd.read_excel('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/TestingData.xlsx')


def NO3():
    # Load the trained model
    model = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulityNO3.h5')

    #print(new_data)

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

    # Predict pH values for the new data
    predicted_NO3_scaled = model.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_NO3_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_NO3_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, NO3_value in enumerate(predicted_NO3_original_scale):
        print(f'Data Point {i+1}: Predicted NO3 = {NO3_value[0]}')

def O2Dis(): 
    # Load the trained model
    model1 = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulityO2-Dis.h5')
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

    # Predict pH values for the new data
    predicted_O2Dis_scaled = model1.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_O2Dis_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_O2Dis_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, O2Dis_value in enumerate(predicted_O2Dis_original_scale):
        print(f'Data Point {i+1}: Predicted O2Dis = {O2Dis_value[0]}')

def pH():
    model2 = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulityPH.h5')
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

    # Predict pH values for the new data
    predicted_pH_scaled = model2.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_pH_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_pH_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, ph_value in enumerate(predicted_pH_original_scale):
        print(f'Data Point {i+1}: Predicted pH = {ph_value[0]}')

def SO4(): 
    model3 = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulitySO4-Tot.h5')
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

    # Predict pH values for the new data
    predicted_SO4_scaled = model3.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_SO4_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_SO4_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, SO4_value in enumerate(predicted_SO4_original_scale):
        print(f'Data Point {i+1}: Predicted SO4 = {SO4_value[0]}')

def TN():
    model4 = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulityTN.h5')
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

    # Predict pH values for the new data
    predicted_TN_scaled = model4.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_TN_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_TN_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, TN_value in enumerate(predicted_TN_original_scale):
        print(f'Data Point {i+1}: Predicted TN = {TN_value[0]}')

def TP():
    model5 = load_model('/Users/aditya/Documents/SRH/Case Study 1/19Sep2023/WaterQulityTP.h5')
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

    # Predict pH values for the new data
    predicted_TP_scaled = model5.predict(X_new_windowed)

    # Inverse transform the scaled predictions to get the original pH values
    predicted_TP_original_scale = scaler_rain.inverse_transform(np.concatenate((predicted_TP_scaled, X_new_scaled[window_size:, 1:]), axis=1))

    # Print the predicted pH values
    for i, TP_value in enumerate(predicted_TP_original_scale):
        print(f'Data Point {i+1}: Predicted TP = {TP_value[0]/100}')




NO3()
O2Dis()
pH()
SO4()
TN()
TP()
