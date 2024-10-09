import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, LSTM
from tensorflow.keras.optimizers import Adam


def preprocess_data(final_data):
    """Preprocess the data: Scaling, Splitting, and Reshaping."""
    # Filtering only numerical columns
    final_data = final_data.select_dtypes(include=[np.number])

    # Data Preparation
    X = final_data[['prcp']]  # Features (assuming 'prcp' is numerical)
    y = final_data.drop(['prcp'], axis=1)  # Targets

    # Scaling the features and targets
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_scaled = scaler_X.fit_transform(X_train)
    y_scaled = scaler_y.fit_transform(y_train)

    # Reshaping the data for Conv1D and LSTM layers
    X_scaled = np.expand_dims(X_scaled, axis=2)

    return X_scaled, y_scaled, X_test, y_test, scaler_X, scaler_y


def build_cnn_lstm_ml_model(input_shape, n_output):
    """Build the CNN-LSTM-ML model."""
    model = Sequential([
        Conv1D(filters=16, kernel_size=1, activation='relu', input_shape=input_shape),
        LSTM(64, return_sequences=True, activation='relu'),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(n_output)
    ])
    return model


def train_cnn_lstm_ml_model(model, X, y, epochs=50, batch_size=16):
    """Train the CNN-LSTM-ML model."""
    opt = Adam(learning_rate=0.001)
    model.compile(optimizer=opt, loss='mean_squared_error')
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
    return model


def evaluate_model(model, X_test, y_test, scaler_X, scaler_y):
    """Evaluate the trained model."""
    X_test_scaled = scaler_X.transform(X_test)
    X_test_scaled = np.expand_dims(X_test_scaled, axis=2)
    y_test_scaled = scaler_y.transform(y_test)
    y_pred_scaled = model.predict(X_test_scaled)

    # Compute MSE and R^2 score for each target variable
    mse_cnn = mean_squared_error(y_test_scaled, y_pred_scaled, multioutput='raw_values')
    r2_cnn = r2_score(y_test_scaled, y_pred_scaled, multioutput='variance_weighted')

    target_cols = y_test.columns.tolist()
    mse_cnn_dict = {col: mse_val for col, mse_val in zip(target_cols, mse_cnn)}

    return mse_cnn_dict, r2_cnn


def predict_new_data(model, new_data, scaler_X):
    """Predict using the trained model on new data."""
    new_data_scaled = scaler_X.transform(new_data)
    new_data_scaled = np.expand_dims(new_data_scaled, axis=2)
    predicted_scaled = model.predict(new_data_scaled)
    return predicted_scaled
