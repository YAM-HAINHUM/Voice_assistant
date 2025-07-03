# === FILE: calendar_manager.py === 
from __future__ import print_function
import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, start_time_str, duration_minutes=60):
    try:
        service = get_calendar_service()

        try:
            start_time = datetime.datetime.strptime(start_time_str.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM'.")

        end_time = start_time + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': summary,
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return created_event.get('htmlLink')

    except Exception as e:
        print("❌ Exception in create_event:", e)
        raise

def list_today_events():
    try:
        service = get_calendar_service()

        now = datetime.datetime.utcnow()
        start = datetime.datetime.combine(now.date(), datetime.time.min).isoformat() + 'Z'
        end = datetime.datetime.combine(now.date(), datetime.time.max).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary', timeMin=start, timeMax=end,
            singleEvents=True, orderBy='startTime').execute()

        events = events_result.get('items', [])
        return events

    except Exception as e:
        print("❌ Failed to list events:", e)
        return []
