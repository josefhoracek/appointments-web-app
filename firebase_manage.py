"""This module is a collection of helper functions that allow the admin to
manage the Firestore database for the appointment scheduler directly from
the development environment.

It is used to create and delete mock availability entries for testing.

Until I add the ability to add and delete availability entries from the web app,
this module is the only way to manage the database.
"""


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from dateutil import tz


def init_db():
    """Initialize the Firestore database."""
    # initialize Firebase using default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    fs = firestore.client()
    return fs

def add_doc(fs, iso_time):
    """Add a document to the database. The time is in ISO format in local tz."""
    to_datetime = datetime.fromisoformat(iso_time)
    datetime_local = to_datetime.replace(tzinfo=tz.gettz('America/Chicago'))
    datetime_UTC = datetime_local.astimezone(tz.UTC)
    coll_ref = fs.collection("appointments")
    update_time, dict_ref = coll_ref.add({
                 "time": datetime_UTC,
                 "firstname": None,
                 "lastname": None,
                 "email": None,
                 "purpose": None,
                 "format": None
                 })

def get_docs(fs):
    """Get all documents from the database."""
    docs = fs.collection("appointments").stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

def delete_doc(fs, doc_id):
    """Delete a document from the database."""
    fs.collection("appointments").document(doc_id).delete()
    print(f'Document {doc_id} deleted.')

def delete_all_docs(fs):
    """Delete all documents from the database."""
    docs = fs.collection("appointments").stream()
    for doc in docs:
        fs.collection("appointments").document(doc.id).delete()
    print('All documents deleted.')

def retrieve_doc(fs, doc_id):
    """Retrieve a document from the database."""
    doc = fs.collection("appointments").document(doc_id).get()
    print(f'{doc.id} => {doc.to_dict()}')

# finish this function
def find_doc(fs, field, value):
    """Find a document in the database."""
    current_date = datetime.date.today()
    next_day = current_date + datetime.timedelta(days=1)
    
    docs_ref = fs.collection("appointments")
    docs = docs_ref.where('time', '>=', next_day.isoformat()).stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

fs = init_db()
# add_doc(fs, '2024-09-23T11:30')
# add_doc(fs, '2024-09-23T12:00')
# add_doc(fs, '2024-09-23T12:30')
# add_doc(fs, '2024-09-23T13:00')
# add_doc(fs, '2024-09-23T13:30')
# get_docs(fs)
delete_doc(fs, 'Es7ktHPYgksLWR9ja9S0')
delete_doc(fs, 'P0rd7ESZsbhyUpeCX8Ot')
delete_doc(fs, 'PCxAEWT6FFc1UOyeAxyI')
# retrieve_doc(fs, 'ZpQMaHgc0TrYLen9IPbU')
# find_doc(fs, 'time', '2221-06-25T00:00:00')
# delete_all_docs(fs)