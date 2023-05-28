from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the LSTM model
loaded_model = load_model('lstm_model.h5')

# Endpoint for loading the model
@app.route('/load_model', methods=['GET'])
def load_model():
    global loaded_model
    loaded_model = load_model('lstm_model.h5')
    return jsonify({'message': 'Model loaded successfully.'})

# Endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the input data

    # Preprocess the input data if required
    # ...

    # Perform prediction using the loaded model
    # Make sure to preprocess the input data in the same way as during training
    # prediction = loaded_model.predict(...)
    
    # Process the prediction results as desired
    # ...

    # Assuming prediction is a numpy array with shape (1, num_timesteps, 2)
    prediction = np.array([[[0.7, 0.9]]])  # Sample prediction values

    # Extract the individual columns from the prediction array
    predicted_finished_clients = prediction[:, :, 0].flatten().tolist()
    predicted_active_clients = prediction[:, :, 1].flatten().tolist()

    # Return the prediction result as a JSON response
    return jsonify({'predicted_finished_clients': predicted_finished_clients, 'predicted_active_clients': predicted_active_clients})

# Endpoint for uploading test data
@app.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files['file']  # Get the uploaded file
    df = pd.read_csv(file)  # Read the CSV file into a DataFrame

    # Preprocess the test data if required
    # ...

    # Extract the necessary columns for prediction
    test_data = df['enrolled_clients'].values.reshape(-1, 1)  # Assuming 'enrolled_clients' is the column to forecast

    # Normalize the test data using the scaler used during training
    test_data = scaler.transform(test_data)

    # Reshape the test data to match the input shape expected by the LSTM model
    test_data = test_data.reshape(1, test_data.shape[0], 1)

    # Make predictions on the test data
    predictions = loaded_model.predict(test_data)

    # Rescale the predictions to the original scale
    predictions = scaler.inverse_transform(predictions)

    # Process the prediction results as desired
    # ...

    return jsonify({'message': 'Test data uploaded successfully.'})

if __name__ == '__main__':
    app.run()
