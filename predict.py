import pandas as pd
import joblib
import os

def preprocess_input(data, label_encoder):
    try:
        data['CAN_ID'] = label_encoder.transform(data['CAN_ID'])
    except ValueError as e:
        print(f"Warning: CAN_ID not seen during training: {e}")
        data['CAN_ID'] = 0  # Fallback for unseen CAN_IDs
    for i in range(8):
        data[f'DATA{i}'] = data[f'DATA{i}'].apply(lambda x: int(x, 16) if isinstance(x, str) and x.strip() else 0)
    data['Timestamp'] = (data['Timestamp'] - data['Timestamp'].min()) / (data['Timestamp'].max() - data['Timestamp'].min())
    return data

def predict(data, model_path, encoder_path):
    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    data = preprocess_input(data.copy(), label_encoder)
    features = ['Timestamp', 'CAN_ID', 'DLC'] + [f'DATA{i}' for i in range(8)]
    X = data[features]
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]
    return predictions, probabilities

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "rf_model.pkl")
    ENCODER_PATH = os.path.join(BASE_DIR, "saved_models", "label_encoder.pkl")
    sample_data = pd.DataFrame({
        'Timestamp': [0.0],
        'CAN_ID': ['0316'],
        'DLC': [8],
        'DATA0': ['05'],
        'DATA1': ['20'],
        'DATA2': ['ea'],
        'DATA3': ['0a'],
        'DATA4': ['20'],
        'DATA5': ['1a'],
        'DATA6': ['00'],
        'DATA7': ['7f']
    })
    predictions, probabilities = predict(sample_data, MODEL_PATH, ENCODER_PATH)
    print(f"Predictions: {predictions}")
    print(f"Attack Probabilities: {probabilities}")