import sounddevice as sd
import wavio

def record_audio(filename="user_audio.wav", duration=5, fs=44100):
    print("Recording started...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"Recording saved as {filename}")

if __name__ == "__main__":
    record_audio()
