# === FILE: gui_dashboard.py ===
import tkinter as tk
from tkinter import ttk

class AssistantDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant Dashboard")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.weather_label = ttk.Label(root, text="Weather: ", font=("Arial", 12))
        self.weather_label.pack(pady=5)

        self.mood_label = ttk.Label(root, text="Mood: ", font=("Arial", 12))
        self.mood_label.pack(pady=5)

        ttk.Label(root, text="Reminders:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.reminders_text = tk.Text(root, height=5, width=60)
        self.reminders_text.pack(pady=5)

        ttk.Label(root, text="Events:", font=("Arial", 11, "bold")).pack(pady=(10, 0))
        self.events_text = tk.Text(root, height=5, width=60)
        self.events_text.pack(pady=5)

    def update_weather(self, info):
        self.weather_label.config(text=f"Weather: {info}")

    def update_mood(self, mood):
        self.mood_label.config(text=f"Mood: {mood}")

    def update_reminders(self, reminders):
        self.reminders_text.delete(1.0, tk.END)
        self.reminders_text.insert(tk.END, "\n".join(reminders))

    def update_events(self, events):
        self.events_text.delete(1.0, tk.END)
        self.events_text.insert(tk.END, "\n".join(events))
