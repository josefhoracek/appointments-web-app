from data import Data
from datetime import datetime, timedelta
from dateutil import tz


class Scheduler:
    """Class to handle the process of appointment scheduling. Converts between
    UTC and user's timezone and between datetime and formatted string."""
    def __init__(self):
        """Initialize a database and set the user's timezone."""
        self.db = Data()
        self.user_tz = tz.gettz('America/Chicago')
    
    def get_availability(self):
        """Return a formatted list of available time slots starting with 
        24hr after user's current time."""
        current_datetime_UTC = self.get_UTC_datetime()
        start_time = current_datetime_UTC + timedelta(hours=24)

        availability = self.db.get_availability(start_time)
        for timeslot in availability:
            timeslot[1] = self.convert_datetime(timeslot[1])
        return availability

    def get_selected_timeslot(self, selected_id):
        """Return the selected timeslot, formatted."""
        selected_timeslot = self.db.get_selected_timeslot(selected_id)
        selected_timeslot[1] = self.convert_datetime(selected_timeslot[1])
        return selected_timeslot

    def get_appointments(self):
        """Return a formatted list of user's upcoming appointments."""
        current_datetime_UTC = self.get_UTC_datetime()
        appointments, last_page = self.db.get_appointments(current_datetime_UTC)
        for appointment in appointments:
            appointment['time'] = self.convert_datetime(appointment['time'])
        return appointments, last_page
    
    def get_previous_appointments(self):
        """Return a formatted, paginated list of user's past appointments."""
        current_datetime_UTC = self.get_UTC_datetime()
        appointments, last_page = self.db.get_previous_appointments()
        for appointment in appointments:
            appointment['time'] = self.convert_datetime(appointment['time'])
        return appointments, last_page

    def convert_datetime(self, UTC_datetime):
        """Convert datetime from UTC to selected timezone and format it as a
        string for readability."""
        user_datetime = UTC_datetime.astimezone(self.user_tz)
        formatted_time = user_datetime.strftime('%A, %B %-d, %Y at %-I:%M %p')
        return formatted_time
    
    def get_UTC_datetime(self):
        """Return user's current datetime in UTC."""
        current_datetime_usertz = datetime.now(tz=self.user_tz)
        current_datetime_UTC = current_datetime_usertz.astimezone(tz.UTC)
        return current_datetime_UTC