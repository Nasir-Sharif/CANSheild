from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import numpy as np
from model.predict import predict

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "saved_models", "rf_model.pkl")
ENCODER_PATH = os.path.join(os.path.dirname(__file__), "model", "saved_models", "label_encoder.pkl")

def convert_to_python_types(value):
    """Convert NumPy types to native Python types."""
    if isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, np.floating):
        return float(value)
    elif isinstance(value, np.ndarray):
        return value.tolist()
    return value

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.json
        df = pd.DataFrame(data)
        predictions, probabilities = predict(df, MODEL_PATH, ENCODER_PATH)
        return jsonify({
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist()
        })
    except Exception as e:
        print(f"Predict error: {str(e)}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            error = 'No file part in the request'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400
        file = request.files['file']
        if file.filename == '':
            error = 'No file selected'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400
        if not file.filename.endswith('.csv'):
            error = 'File must be a .csv'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400

        try:
            df = pd.read_csv(file, dtype={
                'Timestamp': float,
                'CAN_ID': str,
                'DLC': int,
                'DATA0': str, 'DATA1': str, 'DATA2': str, 'DATA3': str,
                'DATA4': str, 'DATA5': str, 'DATA6': str, 'DATA7': str
            }, keep_default_na=False)
        except Exception as e:
            error = f'Failed to read CSV: {str(e)}'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400

        required_columns = ['Timestamp', 'CAN_ID', 'DLC', 'DATA0', 'DATA1', 'DATA2', 'DATA3', 'DATA4', 'DATA5', 'DATA6', 'DATA7']
        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            error = f'CSV missing columns: {", ".join(missing_cols)}'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400

        if df.empty:
            error = 'CSV file is empty'
            print(f"Upload error: {error}")
            return jsonify({'error': error}), 400

        df.fillna({'Timestamp': 0.0, 'CAN_ID': '0000', 'DLC': 0, 'DATA0': '00', 'DATA1': '00',
                   'DATA2': '00', 'DATA3': '00', 'DATA4': '00', 'DATA5': '00', 'DATA6': '00', 'DATA7': '00'}, inplace=True)

        predictions, probabilities = predict(df, MODEL_PATH, ENCODER_PATH)

        results = []
        for i in range(len(df)):
            results.append({
                'Timestamp': convert_to_python_types(df['Timestamp'].iloc[i]),
                'CAN_ID': convert_to_python_types(df['CAN_ID'].iloc[i]),
                'DLC': convert_to_python_types(df['DLC'].iloc[i]),
                'DATA0': convert_to_python_types(df['DATA0'].iloc[i]),
                'DATA1': convert_to_python_types(df['DATA1'].iloc[i]),
                'DATA2': convert_to_python_types(df['DATA2'].iloc[i]),
                'DATA3': convert_to_python_types(df['DATA3'].iloc[i]),
                'DATA4': convert_to_python_types(df['DATA4'].iloc[i]),
                'DATA5': convert_to_python_types(df['DATA5'].iloc[i]),
                'DATA6': convert_to_python_types(df['DATA6'].iloc[i]),
                'DATA7': convert_to_python_types(df['DATA7'].iloc[i]),
                'Prediction': 'Normal' if predictions[i] == 0 else 'Attack',
                'Attack_Probability': round(float(probabilities[i]), 2)
            })

        print(f"Successfully processed {len(results)} rows")
        return jsonify({'results': results})
    except Exception as e:
        error = f'Upload error: {str(e)}'
        print(f"Upload error: {error}")
        return jsonify({'error': error}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)