import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Data:
    """Class to handle database operations. Datetime is stored 
    as UTC datetime."""
    def __init__(self):
        """Initialize a Firestore database to access availability and 
        appointments."""
        # initialize Firebase using default credentials
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        self.fs = firestore.client()
        self.coll_ref = self.fs.collection("appointments")
        self.first_doc = None
        self.last_doc = None

    def get_availability(self, start_time):
        """Return a list of available times and their IDs, starting from 
        a given time."""
        query = (self.coll_ref.where('time', '>=', start_time)
                 .where('firstname', '==', None))
        results = query.stream()

        availability = []
        for result in results:
            availability.append([result.id, result.to_dict()['time']])
        return availability
    
    def get_selected_timeslot(self, selected_id):
        """Return the selected timeslot."""
        result = self.coll_ref.document(selected_id).get()
        timeslot = [result.id, result.to_dict()['time']]
        return timeslot
    
    def write_appointment(self, selected_id, firstname, lastname, email, 
                          purpose, format):
        """Write an appointment to the database."""
        self.coll_ref.document(selected_id).update({
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "purpose": purpose,
            "format": format
            })
    
    def get_appointments(self, current_datetime):
        """Return a page of upcoming appointments or a subsequent page."""
        if not self.last_doc:
            self.last_doc = current_datetime
        query = (self.coll_ref
                .where('firstname', '>', '')
                .order_by('time')
                .start_after({'time': self.last_doc})
                .limit(6)) 
            # read one more than needed to determine if there is a next page
        results = query.stream()
        appointments = []
        for result in results:
            appointments.append(result.to_dict())
        if appointments:
            if len(appointments) == 6:
                last_page = False
                appointments.pop() # remove the extra result
            else:
                last_page = True
            self.first_doc = appointments[0]['time']
            self.last_doc = appointments[-1]['time']
        else:
            last_page = True
        return appointments, last_page
    
    def get_previous_appointments(self):
        """Return a previous page of appointments."""
        query = (self.coll_ref
                .where('firstname', '>', '')
                .order_by('time', direction=firestore.Query.DESCENDING)
                .start_after({'time': self.first_doc})
                .limit(6))
        results = query.stream()
        appointments = []
        for result in results:
            appointments.append(result.to_dict())
        if appointments:
            if len(appointments) == 6:
                last_page = False
                appointments.pop()
            else:
                last_page = True
            appointments.reverse()
            self.first_doc = appointments[0]['time']
            self.last_doc = appointments[-1]['time']
        else:
            last_page = True
        return appointments, last_page