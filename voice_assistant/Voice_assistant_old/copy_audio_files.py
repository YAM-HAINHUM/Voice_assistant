import shutil

# Adjust paths to where your actual files are stored
source_folder = "C:/Users/URMILA/Downloads/"
target_dataset = "C:/Users/URMILA/OneDrive/Documents/Desktop/Voice_Assistance/audio_dataset/"

emotion_files = {
    "happy": "happy.wav",
    "sad": "sad.wav",
    "angry": "angry.wav",
    "neutral": "neutral.wav"
}

for emotion, filename in emotion_files.items():
    src = source_folder + filename
    dst = target_dataset + emotion + "/" + filename
    try:
        shutil.copy(src, dst)
        print(f"✅ Copied {filename} to {emotion} folder.")
    except Exception as e:
        print(f"❌ Failed to copy {filename}: {e}")
