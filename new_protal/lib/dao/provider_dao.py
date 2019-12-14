import pickle
from abc import ABC, abstractmethod
from lib.appointment import Appointment
from lib.centre import Centre
from lib.user import Provider

class CentreDao(ABC):
    @abstractmethod
    def add_centre(self, centre):
        pass

    @abstractmethod
    def add_provider(self, provider):
        pass

    @abstractmethod
    def add_provider_centre(self, provider):
        pass

    # @abstractmethod
    # def validate_login(self, username, password):
    @abstractmethod
    def search_by_centre(self, search_string):
        pass

    @abstractmethod
    def append_appointment(self,name, appointment):
        pass

    @abstractmethod
    def search_by_service(self, search_string):
        pass

    @abstractmethod
    def search_by_suburb(self, search_string):
        pass

    @abstractmethod
    def search_by_provider(self, search_string):
        pass

    @abstractmethod
    def search_specialist(self, search_string):
        pass
    @abstractmethod
    def get_centre(self, name):
        pass

    @abstractmethod
    def get_provider(self, name):
        pass

    @abstractmethod
    def is_exist(self, name):
        pass
    # @abstractmethod
    # def find_by_id(self, id):


    @abstractmethod
    def max_id(self):
        pass

    def save_data(self):
        pass

    @classmethod
    @abstractmethod
    def load_data(cls):
        pass


class CentreManager(CentreDao):
    def __init__(self):
        self._appointments = []
        self._centres = {}
        self._providers = {}

    @property
    def appointments(self):
        return self._appointments

    def append_appointment(self, name, appointment):
        print(name)
        print(appointment)
        self._appointments.append(appointment)
        print(self._appointments)

    @property
    def centre(self):
        return self._centres

    def add_centre(self, centre):
            self._centres[centre.name] = centre

    def add_provider(self, provider):
        if self.is_exist(provider.username) == False:
            self._providers[provider.username] = provider

    def add_provider_centre(self, centre, username):
        provider = self._providers.get(username)
        provider.add_centre(centre)
        temp_centre = self._centres.get(centre)
        temp_centre.add_provider(provider)


    def is_exist(self, name):
        if name in self._providers:
            return True
        else:
            return False

    def search_by_centre(self, search_string):
        return [values for values in self._centres.values()
                if search_string.lower() in values.name.lower()
                ]

    def search_by_service(self, search_string):
        return [values for values in self._providers.values()
                    if search_string.lower() in values.service.lower()
                ]

    def search_by_suburb(self, search_string):
        return [values for values in self._centres.values()
                    if search_string.lower() in values.suburb.lower()
                ]


    def search_by_provider(self, search_string):
        return [values for values in self._providers.values()
                    if search_string.lower() in values.username.lower()
                ]

    def search_specialist(self, search_string):
        return [i for i in self._providers.values()
                    if i.__class__.__name__ == "Specialist" and ( search_string.lower() in i.username.lower() or  search_string.lower() in i.service.lower())]

    def get_centre(self, name):
        for values in self._centres.values():
            if values.name == name:
                return values
        # Not necessary but explicit
        return None

    def get_provider(self, name):
        for values in self._providers.values():
            if values.username == name:
                return values
        # Not necessary but explicit
        return None

    # def find_by_id(self, id):
        # for i in self._centres.values():
            # if i.get_id() == id:
                # return i
        #Not necessary but explicit


    def max_id(self):
        return max([int(values.get_id()) for values in self._centres.values()])

    def save_data(self):
        print("hello")
        print(self._appointments)
        print(self._providers)
        with open('centres.dat', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_data(cls):
        try:
            with open('centres.dat', 'rb') as file:
                centremanager = pickle.load(file)
            Centre.set_id(centremanager.max_id())
        except IOError:
            centremanager = CentreManager()
        return centremanager
