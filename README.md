# Appointments Web App

**A bare-bones, easy-to-use web app for scheduling appointments.** 

I wrote the app for my own use and currently run it at 
[appointments.horacek.info](https://appointments.horacek.info). 
The goal was to make it as simple and friction-free for the user as possible.

## How it works:
1. As an admin, I add time slots to indicate availability.
1. I give the app URL to users who want to make an appointment with me.
1. Users access the app and select an available time slot. (Users cannot make an
appointment sooner than 24 hours before current datetime.)
1. After selecting a time slot, users enter their info (name, email, 
meeting format: in-person or remote). A confirmation page will display.
1. I access the app, log in as admin, and view my scheduled appointments starting
with current datetime. I can also browse my old appointments in a paginated view.

All time slots display in a single, hard-coded timezone regardless of the user's
location.

## Future enhancements:
- Add and delete availablility from the admin interface on the web. 
(Currently, I do this by calling Python methods from the IDE.)
- Check the app for privacy and security as well as accessibility.
- Email and calendar integration.
- Work with any timezone.
- Cancel or reschedule appointments from the admin interface.
- Allow appointments of different lengths (currently they are all 30 minutes,
which serves my purpose).
- Write some tests.

Making the app available to other users would require storing 
admin-level users and their logins in the database, creating new database 
tables/documents for their appointments, and writing a how-to. At that point, 
I may need to spruce up the graphic design and come up with a clever name for 
the app :))

## What I'm learning from this project:
- Databases: I wrote a version to run locally using sqlite (an SQL database) and
then switched to Google Firestore (a NoSQL database) for the web version.
- Datetime and timezone operations in Python.
- Implementing web forms in Flask/Python.
- Bootstrap 5.3.3 but keeping styling real simple. 

## Tools I've used (tech stack):
- Python
- Flask/Jinja
- HTML/CSS/Bootstrap
- Firestore
- Google AppEngine
- PorkBun/CloudFlare
- git/GitHub