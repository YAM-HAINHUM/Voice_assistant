# location_reminder.py
from geopy.distance import geodesic
from config import LOCATION_REMINDER, LOCATION_THRESHOLD_KM

class LocationReminder:
    def __init__(self, user_location):
        """
        user_location: tuple of (latitude, longitude)
        """
        self.user_location = user_location

    def check_reminders(self):
        reminders_to_trigger = []
        for place, info in LOCATION_REMINDER.items():
            place_coords = (info["lat"], info["lon"])
            distance = geodesic(self.user_location, place_coords).km
            if distance <= LOCATION_THRESHOLD_KM:
                reminders_to_trigger.append(info["reminder"])
        return reminders_to_trigger
