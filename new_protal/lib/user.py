from flask_login import UserMixin, current_user, login_required, login_user, logout_user
from lib.appointment import *
import datetime
class User(UserMixin):
    __id = -1

    def __init__(self, username, password, fullname, phonenum, admin):
        self._id = self._generate_id()
        self._username = username
        self._password = password
        self._admin = admin
        self._appointments = []
        self._fullname = fullname
        self._phonenumber = phonenum

    # Object encalsulation attribute (Property)
    @property
    def username(self):
        return self._username
    @property
    def id(self):
        return self._id
    @property
    def type(self):
        return self._type
    @property
    def appointments(self):
        return self._appointments
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    @property
    def admin(self):
        return self._admin
    @property
    def fullname(self):
        return self._fullname
    @property
    def phone_number(self):
        return self._phonenumber
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @admin.setter
    def admin(self, status):
        self._admin = status

    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        User.__id += 1
        return User.__id

    @classmethod
    def set_id(cls, id):
        cls.__id = id

    def validate_password(self, password):
        return self._password == password

    def append_appointment(self, appointment):
        self._appointments.append(appointment)

    def check_available(self,date,time):

        # if (self._admin == True):
        for i in self._appointments:
            if (time == i.time and date == i.date):
                return False
        return True
        # return False

    # edit personal information
    def edit_personal_info(self, name, phone):
        self._fullname = name
        self._phonenumber = phone

    def edit_username(self,new_username):
        self._username = new_username
    def edit_fullname(self,new_name):
        self._fullname = new_name
    def edit_phone_num(self,new_num):
        self._phonenumber = new_num

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # sort appointment list by date and time
    def sort_appointment_list(self):
        app_list = self.appointments
        # sort list by time
        sorted_time = sorted(app_list, key=lambda x: datetime.datetime.strptime(x.time, '%H:%M'))
        # sort list by date
        sorted_date = sorted(sorted_time, key=lambda x: datetime.datetime.strptime(x.date, '%Y-%m-%d'))
        return sorted_date

#----------------------------------------------------------------------------------------------------------------------------
class Patient(User):
    def __init__(self, username, password,fullname, phonenum):
        User.__init__(self, username, password, fullname, phonenum, admin = False)
        self._descriptions = {}
        self._descriptions_time = {}
        self._med_prescriptions = {}

    @property
    def descriptions(self):
        return self._descriptions

    @property
    def descriptions_time(self):
        return self._descriptions_time

    @property
    def med_prescriptions(self):
        return self._med_prescriptions

    def add_description(self, name, script, time, med):
        # del self._descriptions[name]
        # del self._descriptions_time[name]
        for appointment in self._appointments:
            if name == appointment.provider.username:
                self._descriptions[name] = script
                self._descriptions_time[name] = time
                self._med_prescriptions[name] = med
                return True

        return False

class Provider(User):
    def __init__(self, username, password, centre, service, fullname, phonenum):
        User.__init__(self, username, password, fullname, phonenum, admin =True)
        self._centre = [centre]
        self._service = service
        self._rate = { "monkey" : 5 }
        # add working hour
        self._start_hour = {}
        self._finish_hour = {}

    @property
    def service(self):
        return self._service

    @property
    def centre(self):
        return self._centre
#
    @property
    def rate(self):
        lenth = 0
        sumrate = 0
        for values in self._rate.values():
            sumrate += int(values)
            lenth += 1
        return sumrate/lenth

    def get_hour(self,centre):
        return self._start_hour[centre], self._finish_hour[centre]


    # @property
    # def rate(self):
        # return self._rate

    def add_centre(self, centre):
        self._centre.append(centre)

    # def check_available(self,date,time):
    #     for i in self._appointments:
    #         if (time == i.time and date == i.date):
    #             return False
    #     return True

    def complete_treatment(self,name, date, time):
        for i in self._appointments:
            if i.patient.username == name and i.date == date and i.time == time:
                i.close_status()

    def make_rate(self, name, rate):
        # if self._rate.get(name) is not None:

        self._rate[name] = rate

    def add_workhour(self,key,start,end):
        self._start_hour[key] = int(start)
        self._finish_hour[key] = int(end)

class Specialist(Provider):
    def __init__(self, username, password, centre, service, fullname, phonenum):
        Provider.__init__(self, username, password, centre,service, fullname, phonenum)
        self._allow_appointment = []


    @property
    def allow_appointment(self):
        return self._allow_appointment

    def add_referral(self, name):
        self._allow_appointment.append(name)


    def check_available(self,date,time):
        if (self._admin == True) and current_user.username in self._allow_appointment:
            for i in self._appointments:
                if (time == i.time and date == i.date):
                    return False
            return True
        return False
