from abc import ABC, abstractmethod
from datetime import datetime



class AppointmentDAO(ABC):
    @abstractmethod
    def close_status(self, centre):
        pass

    @abstractmethod
    def is_closed(self, provider):
        pass

    @abstractmethod
    def delete(self, provider):
        pass




class Appointment(AppointmentDAO):
    def __init__(self, date, time, Centre, provider, services, Booking_description, patient, status, record_note = None, medicine = None):
        self._date = date
        self._time = time
        self._Centre = Centre
        self._provider = provider
        self._sevices = services
        self._booking_desc = Booking_description
        self._patient = patient
        self._record_note = record_note
        self._medicine = medicine
        self._status = status

    # get instances method
    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def centre(self):
        return self._Centre

    @property
    def provider(self):
        return self._provider

    @property
    def services(self):
        return self._sevices

    @property
    def booking_desc(self):
        return self._booking_desc

    @property
    def patient(self):
        return self._patient

    @property
    def record_note(self):
        return self._record_note

    @property
    def medicine(self):
        return self._medicine

    @property
    def status(self):
        return self._status

    def close_status(self):
        self._status = False

    # def delete(self):
    #     if self._provider.check_available(self._date, self._time) and self._patient.check_available(self._date, self._time):
    #         if self.is_closed() == False:
    #             self._provider.append_appointment(self)
    #             self._patient.append_appointment(self)
    #         else:
    #             # date is already passed
    #             del self
    #             return True
    #     else:
    #         # date is unavailable
    #         del self
    #         return True

    def delete(self):
        if self._provider.check_available(self._date, self._time) and self._patient.check_available(self._date, self._time):
            if self.is_closed() == False and (self._provider is not self._patient):
                self._provider.append_appointment(self)
                self._patient.append_appointment(self)
                return None
            else:
                # date is already passed
                #del self
                return "invalid"
        else:
            # date is unavailable
            #del self
            return "unavailable"


    def is_closed(self):
        curr_time = datetime.now()
        cur_year = int(str(curr_time)[0:4])
        cur_month = int(str(curr_time)[5:7])
        cur_day = int(str(curr_time)[8:10])
        cur_hr = int(str(curr_time)[11:13])
        cur_min = int(str(curr_time)[14:16])

        year = int(str(self._date)[0:4])
        month = int(str(self._date)[5:7])
        day = int(str(self._date)[8:10])
        hr = int(str(self._time)[0:2])
        min = int(str(self._time)[3:5])

        closed = True

        if cur_year < year:
            closed = False
        elif cur_year == year:
            if cur_month < month:
                closed = False
            elif cur_month == month:
                if cur_day < day:
                    closed = False
                elif cur_day == day:
                    if cur_hr < hr:
                        closed = False
                    elif cur_hr == hr:
                        if cur_min < min:
                            closed = False
        return closed
