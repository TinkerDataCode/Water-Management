import runpy
import pandas as pd
runpy.run_path('recent_weather_data.py')

# Load the recent_weather_data.csv file
recent_data = pd.read_csv(r"D:/Case_study/CaseStudy_app/new file/new file/recent_weather_data.csv")
prcp_values = recent_data['prcp'].values
time_values = recent_data['time'].values

from Data_modelling import predict_new_data
from tensorflow.keras.models import load_model
import pickle
import numpy as np
#D:\Case_study\CaseStudy_app\new file\new file
#D:\Case_study\CaseStudy_app\new file\new file

model_path = r"D:/Case_study/CaseStudy_app/new file/new file/"
model = load_model(model_path)

with open(r"D:/Case_study/CaseStudy_app/new file/new file/scaler_X.pkl", 'rb') as file:
    scaler_X = pickle.load(file)

with open(r"D:/Case_study/CaseStudy_app/new file/new file/scaler_y.pkl", 'rb') as file:
    scaler_y = pickle.load(file)

with open(r"D:/Case_study/CaseStudy_app/new file/new file/target_cols.pkl", 'rb') as file:
    target_cols = pickle.load(file)

predictions = []

for idx, value in enumerate(prcp_values):
    new_prcp_value = [[value]]
    new_prcp_scaled = scaler_X.transform(new_prcp_value)
    new_prcp_scaled = np.expand_dims(new_prcp_scaled, axis=2)

    # Predict using the trained CNN model
    predicted_scaled = model.predict(new_prcp_scaled)

    # Inverse transform to get the predictions in the original scale
    predicted_original = scaler_y.inverse_transform(predicted_scaled)

    # Save the predicted values
    predicted_dict = {col: pred for col, pred in zip(target_cols, predicted_original[0])}
    predictions.append(predicted_dict)

for idx, prediction in enumerate(predictions):
    print(f"Date: {time_values[idx]} - Predicted values for prcp={prcp_values[idx]}: {prediction}")
