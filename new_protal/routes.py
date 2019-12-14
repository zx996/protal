from functools import wraps
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from server import app, login_manager, user_db, centremanager
from lib.appointment import *
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return user_db.find_by_id(user_id)


def admin_required(f):
    """This is used to check the admin status of the user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.admin:
            return redirect(url_for('page_not_found'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template('home.html')




#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    results = []
    if request.args.get('s') is not None:
        search_string = request.args['s']
        select = request.args.get('select', 'provider')
        if select == 'centre':
            results = centremanager.search_by_centre(search_string)
        elif select == 'service':
            results =centremanager.search_by_service(search_string)
        elif select == 'suburb':
            results =centremanager.search_by_suburb( search_string)
        else:
            results = centremanager.search_by_provider(search_string)

    return render_template('search.html', results=results)

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/profile/<name>/<type>', methods=['GET', 'POST'])
@login_required
def profile(name, type):
    permission = False

    is_themself = False     # flag to separate between the profile of their own or the others
    centre_list = []
    if type == "Centre":
        temp = centremanager.get_centre(name)
        provider_dict = list(temp.providers.values())
    else:
        if type == "Provider" or (type == "Specialist"):
            temp = centremanager.get_provider(name)
            provider_dict = temp.centre[1:]
            print(provider_dict)
            is_themself = "Provider"
            centre_list = temp.centre[1:]
            for idx,i in enumerate(centre_list):
                centre_list[idx] = centremanager.get_centre(i)
            print(centre_list)

        elif type == "Patient":
            temp = user_db.get_patient(name)
            provider_dict = None
            if current_user.username == name:
                permission = True
                is_themself = "Patient"
            for appointment in temp.appointments:
                if appointment.provider.username == current_user.username:
                    permission = True
        # is_themself = True

    if request.method == 'GET' and type != "Patient":
        rate = request.args.get('rate','3')
        print(rate)
        name = current_user.username
        temp.make_rate(name,rate)
    return render_template('profile.html', tempone = temp, provider_dict = provider_dict, permission = permission, ownprofile = is_themself, centre_list = centre_list)

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/edit_profile_info/<type>', methods=["GET", "POST"])
@login_required
def edit_profile(type):

    if type == "Provider" or (type == "Specialist"):
        temp = centremanager.get_provider(current_user.username)
    elif type == "Patient":
        temp = user_db.get_patient(current_user.username)

    # edit button is clicked
    if request.method == "POST":
        curr_username = current_user.username
        fullname = request.form["fullname"]
        phone = request.form["phonenumber"]

        temp.edit_personal_info(fullname, phone)

        print(temp.username)

        # test write file

        #------------------




        return redirect(url_for("profile",name = temp.username , type = type))


    return render_template('edit_profile.html',tempone = temp)

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/booking/<providername>/<centre>', methods=['GET', 'POST'])
@login_required
def booking(providername, centre):
    print("print CENTRE",centre)

    make = False
    error = None

    provider = centremanager.get_provider(providername)
    patient = user_db.get_patient(current_user.username)
    date = datetime.now()
    todaydate = str(date)[0:10]
    if centre != "individual":
        start_time, finish_time = provider.get_hour(centre)
    else:
        start_time = 7
        finish_time = 22

    if request.method == 'POST':
        # Checks the user before logging in
        appointment_date = request.form['date']
        appointment_time = request.form['time']
        if request.form['description']:
            Booking_description = request.form['description']
        else:
            Booking_description = None
        status = True
        service = provider.service
        centrename = centre

        temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
        error = temp_appointment.delete()
        if error == None:
            centremanager.append_appointment(patient.username,temp_appointment)
            make = True

    return render_template('booking.html', provider = provider, make = make, todaydate = todaydate, error = error, start = start_time, finish = finish_time, centre = centre)
#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Checks the user before logging in
        user = user_db.validate_login(request.form['username'], request.form['password'])
        if user is None:
            return render_template('login.html',login_fail="invalid")
        login_user(user)
        # Next helps with redirecting the user to their previous page
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    return render_template('login.html')

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/edit_history/<patientname>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_history(patientname):
    patient = user_db.get_patient(patientname)
    time = int(str(curr_time)[0:16])
    edit_permission = False
    if patient.descriptions[current_user.username] != None:
            edit_permission = True
            history =  patient.descriptions[current_user.username]
    if request.method == 'POST':
        script = request.args['history']
        patient.add_description(current_user.username,script, time )
    return render_template('edit_history.html', permission = edit_permission, history = history )

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    # appointments = current_user.appointments

    # sort an appointment list
    appointments = current_user.sort_appointment_list()

    appointment_list = [i for i in appointments if i.status == True]
    if request.method == 'POST':
        if request.form['action'] == 'close':
            patientname = request.form['patientname']
            date =  request.form['date']
            time = request.form['time']
            current_user.complete_treatment(patientname, date, time)
            return redirect(url_for('appointment'))



    return render_template('appointment.html', appointment_list = appointment_list)

#---------------------------------------------------------------------------------------------------------------------------
@app.route('/referral/<name>', methods=['GET', 'POST'])
@login_required
def referral(name):
    # appointments = current_user.appointments
    results = []
    make = False
    if request.args.get('s') is not None:
        search_string = request.args['s']
        results = centremanager.search_specialist(search_string)

    if request.method == 'POST':
        if request.form['action'] == 'send':
            providernam = request.form['providername']
            provider = centremanager.get_provider(providernam)
            provider.add_referral(name)
            make = True

    return render_template('referral.html', results = results, name = name, make = make)
#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/consultation/<username>/<date>/<time>', methods=['GET','POST'])
@login_required
def consultation(username, date, time):
    patient = user_db.get_patient(username)

    if request.args.get('action')=='close':
        # patientname = request.form['patientname'];
        # date =  request.form['date']
        current_user.complete_treatment(username, date, time)
        return redirect(url_for('appointment'))

    if request.method == "POST":
        script = request.form["recordnote"]
        time = str(datetime.now())[0:16]
        medicine = request.form["medicine"]
        patient.add_description(current_user.username,script,time,medicine)


    return render_template('consultation.html',patient = patient, description = patient.descriptions, time = patient.descriptions_time, med = patient.med_prescriptions)


    if request.method == 'POST':
        if request.form['action'] == 'send':
            providernam = request.form['providername']
            provider = centremanager.get_provider(providernam)
            provider.add_referral(name)
    return render_template('referral.html', results = results, name = name)
#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    # appointments = current_user.appointments
    appointments = reversed(current_user.sort_appointment_list())
    appointment_list = [i for i in appointments if i.status == False]
    return render_template('history.html', appointment_list = appointment_list)

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404

#--------------------------------------------------------------------------------------------------------------------------------
