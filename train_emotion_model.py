import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import joblib

# Paths
DATASET_PATH = "audio_dataset/"
MODEL_PATH = "models/emotion_svm_model.pkl"
EMOTIONS = ['happy', 'sad', 'angry', 'neutral']

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=3, offset=0.5)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfcc_scaled = np.mean(mfccs.T, axis=0)
        return mfcc_scaled
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

features = []
labels = []

for emotion in EMOTIONS:
    emotion_dir = os.path.join(DATASET_PATH, emotion)
    if not os.path.exists(emotion_dir):
        print(f"Missing directory: {emotion_dir}")
        continue
    for filename in os.listdir(emotion_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(emotion_dir, filename)
            mfcc = extract_features(file_path)
            if mfcc is not None:
                features.append(mfcc)
                labels.append(emotion)

# Encode labels and train model
X = np.array(features)
y = LabelEncoder().fit_transform(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
