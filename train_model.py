import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def load_and_label_data(processed_dir):
    datasets = {
        'Attack_free_dataset.csv': 0,  # Normal
        'Fuzzy_attack_dataset.csv': 1,  # Attack
        'Impersonation_attack_dataset_2.csv': 1,  # Attack
        'DoS_attack_dataset_2.csv': 1  # Attack
    }
    dataframes = []
    
    for file, label in datasets.items():
        file_path = os.path.join(processed_dir, file)
        if os.path.exists(file_path):
            # Read in chunks to handle large files
            for chunk in pd.read_csv(file_path, chunksize=10000):
                chunk['Label'] = label
                dataframes.append(chunk)
        else:
            print(f"Warning: File not found: {file_path}. Skipping...")
    
    if not dataframes:
        raise ValueError("No datasets loaded. Check processed directory.")
    
    return pd.concat(dataframes, ignore_index=True)

def preprocess_data(df):
    # Encode CAN_ID (hex to integer)
    le = LabelEncoder()
    df['CAN_ID'] = le.fit_transform(df['CAN_ID'])
    
    # Convert DATA0-DATA7 from hex to integer
    for i in range(8):
        df[f'DATA{i}'] = df[f'DATA{i}'].apply(lambda x: int(x, 16) if isinstance(x, str) and x.strip() else 0)
    
    # Normalize Timestamp
    df['Timestamp'] = (df['Timestamp'] - df['Timestamp'].min()) / (df['Timestamp'].max() - df['Timestamp'].min())
    
    return df, le

def train_model(processed_dir, model_path):
    # Load and label data
    df = load_and_label_data(processed_dir)
    
    # Preprocess data
    df, label_encoder = preprocess_data(df)
    
    # Features and target
    features = ['Timestamp', 'CAN_ID', 'DLC'] + [f'DATA{i}' for i in range(8)]
    X = df[features]
    y = df['Label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # Evaluate
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    print(f"Training Accuracy: {train_score:.4f}")
    print(f"Testing Accuracy: {test_score:.4f}")
    
    # Save model and label encoder
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(rf, model_path)
    joblib.dump(label_encoder, os.path.join(os.path.dirname(model_path), 'label_encoder.pkl'))
    print(f"Model saved to {model_path}")
    print(f"Label encoder saved to {os.path.dirname(model_path)}/label_encoder.pkl")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
    MODEL_PATH = os.path.join(BASE_DIR, "..", "saved_models", "rf_model.pkl")
    
    train_model(PROCESSED_DIR, MODEL_PATH)