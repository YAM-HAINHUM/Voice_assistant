import os
import shutil

# Folder where the .wav files are currently located
source_folder = "audio_dataset/"
target_folders = {
    "happy": "happy.wav",
    "sad": "sad.wav",
    "angry": "anger.wav",  # Assuming you named it 'anger.wav'
    "neutral": "neutral.wav"
}

for emotion, filename in target_folders.items():
    src = os.path.join(source_folder, filename)
    dest_folder = os.path.join(source_folder, emotion)
    dest = os.path.join(dest_folder, f"{emotion}.wav")
    try:
        os.makedirs(dest_folder, exist_ok=True)
        shutil.move(src, dest)
        print(f"✅ Moved {filename} to {dest}")
    except Exception as e:
        print(f"❌ Failed to move {filename}: {e}")
