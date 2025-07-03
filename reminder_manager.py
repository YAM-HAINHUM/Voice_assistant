
# === FILE: reminder_manager.py ===
import json
import time
import threading
import uuid
import os

REMINDER_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, 'r') as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def add_reminder(message, minutes):
    reminder = {
        "id": str(uuid.uuid4()),
        "message": message,
        "timestamp": time.time() + (minutes * 60),
        "status": "pending"
    }
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)
    return reminder["id"]

def list_reminders():
    reminders = load_reminders()
    return [(i+1, r['message'], r['status']) for i, r in enumerate(reminders)]

def cancel_reminder(index):
    reminders = load_reminders()
    if 0 <= index < len(reminders):
        reminders.pop(index)
        save_reminders(reminders)
        return True
    return False

def reminder_checker(speak):
    def check():
        while True:
            reminders = load_reminders()
            now = time.time()
            updated = False
            for r in reminders:
                if r['status'] == 'pending' and now >= r['timestamp']:
                    speak(f"Reminder: {r['message']}")
                    r['status'] = 'done'
                    updated = True
            if updated:
                save_reminders(reminders)
            time.sleep(30)
    threading.Thread(target=check, daemon=True).start()
