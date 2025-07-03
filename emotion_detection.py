import librosa
import numpy as np
import joblib

# Load a trained classifier (SVM or similar). Replace with your actual model path
model = joblib.load("models/emotion_svm_model.pkl")

# List of emotion labels your model predicts
emotions = ['angry', 'happy', 'neutral', 'sad']

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, duration=3, offset=0.5)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_scaled = np.mean(mfcc.T, axis=0)
        return mfcc_scaled
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def predict_emotion(audio_path):
    features = extract_features(audio_path)
    if features is not None:
        prediction = model.predict([features])[0]
        return emotions[prediction]
    return "unknown"
import librosa
import numpy as np
import joblib
import os

MODEL_PATH = "models/emotion_svm_model.pkl"
EMOTIONS = ['happy', 'sad', 'angry', 'neutral']

# Load model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError("Trained model not found. Please run train_emotion_model.py first.")

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, duration=3, offset=0.5)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_scaled = np.mean(mfcc.T, axis=0)
        return mfcc_scaled
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

def predict_emotion(audio_path):
    features = extract_features(audio_path)
    if features is not None:
        label_index = model.predict([features])[0]
        return EMOTIONS[label_index]
    else:
        return "unknown"
