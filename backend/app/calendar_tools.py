from langchain.tools import tool
from datetime import date
from app.services import get_calendar_service, get_available_slots, book_appointment

@tool
def check_calendar_availability(check_date: str) -> list:
    """
    Checks for available 1-hour appointment slots on a given date.
    The date should be in 'YYYY-MM-DD' format.
    """
    service = get_calendar_service()
    return get_available_slots(service, check_date)

@tool
def create_calendar_booking(start_time: str, summary: str) -> str:
    """
    Books an appointment on the Google Calendar at a specified start time.
    The start_time must be in 'YYYY-MM-DDTHH:MM:SS' ISO format.
    The summary is the title of the event.
    """
    service = get_calendar_service()
    event = book_appointment(service, start_time, summary)
    return f"Booking confirmed for '{summary}' at {start_time}}"

