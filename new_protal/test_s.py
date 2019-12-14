import pytest
from lib.health_data import HealthData
from lib.appointment import *
from datetime import datetime

@pytest.fixture
def centremanager_fixture():
    # centremanager = CentreManager()
    # centremanager.add_provider(Provider("anna@gmail.com", 'cs1531', 'Sydney Children Hospital', 'GP', 'Anna Elsa',1000000005))
    # centremanager.add_provider(Provider("sid@gmail.com", 'cs1531', 'Sydney Children Hospital', 'GP', 'Anna Elsa',1000000005))

#
    user_db, centremanager = HealthData.load_data()
    return user_db, centremanager


def test_appointmetn(centremanager_fixture):
    user_db, centremanager = centremanager_fixture
    patient = user_db.get_patient("jack@gmail.com")
    provider = centremanager.get_provider("sid@gmail.com")
    centre = centremanager.get_centre(provider.centre[1])
    assert patient != None
    assert provider != None
    curr_time = datetime.now()
    appointment_date = str(curr_time)[0:10]     #booking at now
    appointment_time = str(curr_time)[11:16]
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre

    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == "invalid"
                              #creat appointment in the past

def test_miltiple_appointment(centremanager_fixture):   #test mulyiple appointment at same time
    user_db, centremanager = centremanager_fixture
    patient = user_db.get_patient("jack@gmail.com")
    provider = centremanager.get_provider("sid@gmail.com")
    centre = centremanager.get_centre(provider.centre[1])
    assert patient != None
    assert provider != None

    curr_time = datetime.now()
    appointment_date = "2018-12-15"
    appointment_time = "09:35:30"
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre
    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == None

    curr_time = datetime.now()
    appointment_date = "2018-12-15"
    appointment_time = "09:35:30"
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre
    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == "unavailable"


#
def test_provider_appointment(centremanager_fixture):   #test book an appointment with themself
    user_db, centremanager = centremanager_fixture
    patient = centremanager.get_provider("sid@gmail.com")
    provider = centremanager.get_provider("sid@gmail.com")
    centre = centremanager.get_centre(provider.centre[1])
    assert patient != None
    assert provider != None

#
#
    curr_time = datetime.now()
    appointment_date = "2018-12-15"
    appointment_time = "09:35:30"
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre
    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == "invalid"



def test_view_history(centremanager_fixture):
    user_db, centremanager = centremanager_fixture
    patient = user_db.get_patient("jack@gmail.com")
    provider = centremanager.get_provider("sid@gmail.com")
    centre = centremanager.get_centre(provider.centre[1])
    assert patient != None
    assert provider != None

    appointment_date = "2018-12-15"
    appointment_time = "09:35:30"
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre
    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == None

    script = "view history"
    time = str(datetime.now())[0:16]
    medicine = "medicine"
    patient.add_description(provider.username,script,time,medicine)
    assert patient.descriptions[provider.username] == "view history"


def test_change(centremanager_fixture):#test change history by unauth
    user_db, centremanager = centremanager_fixture
    patient = user_db.get_patient("jack@gmail.com")
    provider = centremanager.get_provider("sid@gmail.com")
    provider1 = centremanager.get_provider("anna@gmail.com")
    centre = centremanager.get_centre(provider.centre[1])
    assert patient != None
    assert provider != None

    appointment_date = "2018-12-15"
    appointment_time = "09:35:30"
    Booking_description = None
    status = True
    service = provider.service
    centrename = centre
    temp_appointment = Appointment(appointment_date, appointment_time, centrename, provider, service, Booking_description, patient, status)
    assert temp_appointment.delete() == None

    script = "view history"
    time = str(datetime.now())[0:16]
    medicine = "medicine"
    assert patient.add_description(provider1.username,script,time,medicine) == False
