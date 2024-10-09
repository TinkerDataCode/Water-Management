import numpy as np
from Data_Collection import load_water_quality_data_from_excel, load_weather_data_from_csv
from Data_ingestion_and_cleaning import transform_water_quality, transform_weather_data, merge_datasets,rearrange_and_fill_missing
from Data_modelling import preprocess_data, build_cnn_model, train_cnn_model, evaluate_model
import pickle
from tensorflow.keras.models import load_model

# 1. Data Collection
water_quality_file_path = r"D:/Case_study/CaseStudy_app/new file/new file/All_Dataset.xlsx"
weather_data_file_path = r"D:/Case_study/CaseStudy_app/new file/new file/combined_data_all_weather.csv"

water_quality, water_quality_error = load_water_quality_data_from_excel(water_quality_file_path)
weather_data, weather_data_error = load_weather_data_from_csv(weather_data_file_path)

if water_quality_error:
    print("Error loading water quality data:", water_quality_error)
    exit()

if weather_data_error:
    print("Error loading weather data:", weather_data_error)
    exit()

# 2. Data Cleaning and Preprocessing
water_quality_transformed = transform_water_quality(water_quality)
weather_data_transformed = transform_weather_data(weather_data)
final_data = merge_datasets(water_quality_transformed, weather_data_transformed, on_column='Station_Date')
column_order =['Station', 'Sample_Date', 'Station_Date','Cl-Dis', 'Cl-Tot', 'NH4N', 'NO2N', 'NO3N',
       'O2-Dis', 'SO4-Tot', 'TEMP', 'TN', 'TOC', 'TP', 'pH', 'prcp']
final_data = rearrange_and_fill_missing(final_data, column_order)


# 3. Data Modelling
X_scaled, y_scaled, X_test, y_test, scaler_X, scaler_y = preprocess_data(final_data)
input_shape = (X_scaled.shape[1], 1)
n_output = y_scaled.shape[1]
model = build_cnn_model(input_shape, n_output)
model = train_cnn_model(model, X_scaled, y_scaled)

# # 4. Evaluate the Model
# mse_cnn_dict, r2_cnn = evaluate_model(model, X_test, y_test, scaler_X, scaler_y)
# print("MSE for each target variable:", mse_cnn_dict)
# print(f"R^2 score: {r2_cnn}")

# 5. Save the Model and Scalers as Pickle Files
# Saving the Keras model
model_path = r"D:/Case_study/CaseStudy_app/new file/new file"
model.save(model_path)

# Saving scaler_X
with open(r"D:/Case_study/CaseStudy_app/new file/new file/scaler_X.pkl", 'wb') as file:
    pickle.dump(scaler_X, file)

# Saving scaler_y
with open(r"D:/Case_study/CaseStudy_app/new file/new file/scaler_y.pkl", 'wb') as file:
    pickle.dump(scaler_y, file)

# Saving target_cols
with open(r"D:/Case_study/CaseStudy_app/new file/new file/target_cols.pkl", 'wb') as file:
    pickle.dump(y_test, file)

#
if __name__ == "__main__":
    pass  # The operations are executed on import for simplicity, but you can move them inside a main function if desired.
