import os
import datetime
import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")
if not CALENDAR_ID:
    print("ERROR: CALENDAR_ID environment variable is not set.")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/calendar']

SERVICE_ACCOUNT_FILE = os.getenv("CREDENTIALS_PATH", "/code/credentials.json")
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    
    if os.path.exists("credentials.json"):
        SERVICE_ACCOUNT_FILE = "credentials.json"
    
    elif os.path.exists("../credentials.json"):
        SERVICE_ACCOUNT_FILE = "../credentials.json"
    else:
        print(f"ERROR: credentials.json not found at {SERVICE_ACCOUNT_FILE}")
        sys.exit(1)

def get_calendar_service():
    """Creates and returns a Google Calendar service object."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_available_slots(service, date):
    """Gets available time slots for a given date."""
    start_time = datetime.datetime.fromisoformat(date).replace(hour=9, minute=0, second=0).isoformat() + 'Z'
    end_time = datetime.datetime.fromisoformat(date).replace(hour=17, minute=0, second=0).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # For simplicity, let's assume 1-hour slots from 9 AM to 5 PM
    available_slots = []
    for hour in range(9, 17):
        slot_start = datetime.datetime.fromisoformat(date).replace(hour=hour, minute=0, second=0)
        is_booked = False
        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start']['dateTime'].split('Z')[0])
            if event_start.hour == hour:
                is_booked = True
                break
        if not is_booked:
            available_slots.append(slot_start.strftime('%Y-%m-%dT%H:%M:%S'))
            
    return available_slots

def book_appointment(service, start_time_str, summary="Appointment"):
    """Books an appointment on the calendar."""
    start_time = datetime.datetime.fromisoformat(start_time_str)
    end_time = start_time + datetime.timedelta(hours=1)

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata', # Or your timezone
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata', # Or your timezone
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event
