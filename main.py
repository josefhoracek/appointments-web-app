from flask import Flask, render_template, request, session
import os
from dotenv import load_dotenv

from scheduler import Scheduler


app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ['SESSION_KEY']
sch = Scheduler()

@app.route('/')
def index():
    availability = sch.get_availability()
    if availability:
        return render_template('index.html', 
            message='Select a time for a 30-minute appointment with me:', 
            availability=availability)
    else:
        return render_template('index.html', 
            message='No availability listed. Email me to request an appointment!')

@app.route('/client-details', methods=['POST'])
def client_details():
    selected_id = request.form['selected_id']
    selected_timeslot = sch.get_selected_timeslot(selected_id)
    session['selected_timeslot'] = selected_timeslot
    return render_template('client-details.html', 
                           selected_timeslot=selected_timeslot)

@app.route('/confirm', methods=['POST'])
def confirm():
    timeslot = session['selected_timeslot']
    selected_id = timeslot[0]
    time = timeslot[1]
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    purpose = request.form['purpose']
    format = request.form['format']
    sch.db.write_appointment(
        selected_id, first_name, last_name, email, purpose, format)
    return render_template('confirm.html', time=time, first_name=first_name, 
                           purpose=purpose, format=format)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin-index', methods=['POST'])
def admin_index():
    username = request.form['username']
    password = request.form['password']
    if username == os.environ['USERNAME'] and password == os.environ['PASSWORD']:
        return render_template('admin-index.html')
    else:
        return render_template('login.html', error='Invalid credentials.')

@app.route('/manage-avalability')
def manage_availability():
    message = ("Here's where you will be able to add or remove availability.")
    return render_template('manage-availability.html', message=message)


@app.route('/current-appointments')
def current_appointments():
    appointments, last_page = sch.get_appointments()
    if appointments:
        message = ("Your appointments:")
        return render_template('current-appointments.html', message=message,
                            appointments=appointments, last_page=last_page)
    else:
        message = ("No upcoming appointments.")
        return render_template('current-appointments.html', message=message,
                               last_page=True)
    
    
@app.route('/previous-appointments')
def previous_appointments():
    appointments, last_page = sch.get_previous_appointments()
    if appointments:
        message = ("Your appointments:")
        return render_template('previous-appointments.html', message=message,
                               appointments=appointments, last_page=last_page)
    else:
        return render_template('previous-appointments.html', 
                               message='No previous appointments.', 
                               last_page=True)