from emotion_detection import predict_emotion

# You can put any string here; dummy function ignores it
emotion = predict_emotion("dummy.wav")
print(f"Detected Emotion: {emotion}")
