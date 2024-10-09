import pandas as pd
import os
import pandas as pd

# Get the directory where your script is located
script_dir = os.path.dirname(__file__)

# Define the relative path to your CSV file from the script's directory
relative_file_path = '2023-09-11_14-41/samples1.csv'  # Replace with the relative path to your CSV file

# Create the full file path by joining the script directory and relative file path
file_path = os.path.join(script_dir, relative_file_path)



# Read the CSV file with a specific encoding
#file_path = 'D:/Case_study/Case_Study_Latest/2023-09-11_14-41/samples1.csv'  # Replace with the actual path to your CSV file
df_original = pd.read_csv(file_path, encoding='latin-1')

# Group by the index columns and aggregate duplicate values using the mean
aggregated_df = df_original.groupby(["GEMS_Station_Number", "Sample_Date", "Sample_Time", "Depth", "Parameter_Code"]).agg({'Value': 'mean'}).reset_index()

# Pivot the data
pivoted_df = aggregated_df.pivot(index=["GEMS_Station_Number", "Sample_Date", "Sample_Time", "Depth"],
                                 columns="Parameter_Code", values="Value").reset_index()

# Print the pivoted DataFrame
#print(pivoted_df)

# Convert 'Sample_Date' to a datetime object
pivoted_df['Sample_Date'] = pd.to_datetime(pivoted_df['Sample_Date'])



# Extract year and month from 'Sample_Date'
pivoted_df['Year'] = pivoted_df['Sample_Date'].dt.year
pivoted_df['Month'] = pivoted_df['Sample_Date'].dt.month


relative_file_path = "weather_final_data_daily1.csv"
# Read the weather data from a CSV file
weather_file_path = os.path.join(script_dir, relative_file_path)
weather_df = pd.read_csv(weather_file_path)

# Convert the 'Sample_Date' column to datetime
weather_df['Sample_Date'] = pd.to_datetime(weather_df['time'])

# Filter rows where 'STATION_NUMBER' is 'DEU01620'
filtered_df = weather_df[weather_df['Station Number'] == 'DEU01620']

# Extract year and month from the 'Sample_Date' column
filtered_df['Year'] = filtered_df['Sample_Date'].dt.year
filtered_df['Month'] = filtered_df['Sample_Date'].dt.month

# Group by 'STATION_NUMBER', year, and month, calculate the sum of 'prcp', and round it
result_df = filtered_df.groupby(['Station Number', 'Year', 'Month'])['prcp'].sum().reset_index()
result_df['prcp'] = result_df['prcp'].round(2)

# Order the result by year and month
result_df = result_df.sort_values(by=['Year', 'Month'])

print(result_df)


# Remove leading and trailing spaces from 'Station Number' and 'GEMS_Station_Number'
#weather_df['Station Number'] = weather_df['Station Number'].str.strip()
pivoted_df['GEMS_Station_Number'] = pivoted_df['GEMS_Station_Number'].str.strip()

#csv_file_path = 'D:/Case_study/Case_Study_Latest/Pivoted_Data_1634.csv'
#pivoted_df.to_csv(csv_file_path, index=True, encoding='utf-8')

#csv_file_path = 'D:/Case_study/Case_Study_Latest/Weather_Data_1634.csv'
#weather_df.to_csv(csv_file_path, index=True, encoding='utf-8')

import pandas as pd

# Assuming 'result_df' and 'pivoted_df' are your DataFrames

# Shift the 'Month' column in 'result_df' by one month to represent the next month
result_df['Next_Month'] = result_df['Month'] + 1

# If 'Month' is 12, set 'Next_Month' to 1 for the next year
result_df.loc[result_df['Next_Month'] == 13, 'Next_Month'] = 1
result_df['Year'] = result_df['Year'] + (result_df['Month'] + 1 > 12).astype(int)

# Merge 'pivoted_df' and 'result_df' based on 'GEMS_Station_Number', 'Year', and 'Next_Month'
combined_df = pd.merge(pivoted_df, result_df, left_on=['GEMS_Station_Number', 'Year', 'Month'],
                       right_on=['Station Number', 'Year', 'Next_Month'])

# Drop the 'Next_Month' column from the merged DataFrame if not needed
combined_df.drop(columns=['Next_Month'], inplace=True)




# Drop the redundant time column
#combined_df.drop(columns=["time"], inplace=True)

# Assuming combined_df is your DataFrame
columns_to_keep = ['NO3N', 'O2-Dis', 'SO4-Tot', 'TEMP', 'TP', 'pH', 'TN', 'prcp','Sample_Date','GEMS_Station_Number']
combined_df = combined_df[columns_to_keep] 
# Print the combined DataFrame
print(combined_df)


# Define the relative path to your CSV file from the script's directory
relative_file_path = 'Combined_Data_Final3.csv'  # Replace with the relative path to your CSV file

# Create the full file path by joining the script directory and relative file path
csv_file_path = os.path.join(script_dir, relative_file_path)

#csv_file_path = 'D:/Case_study/CaseStudy_app/New_Data/Combined_Data_Final3.csv'

combined_df.to_csv(csv_file_path, index=True, encoding='utf-8')