from abc import ABC, abstractmethod
from lib.user import *
from lib.appointment import Appointment
class Centre(ABC):
    __id = -1

    def __init__(self,centre_type, abn, name, phone, suburb):
        self._id = self._generate_id()
        self._centre_type = centre_type
        self._abn = abn
        self._name = name
        self._phone = phone
        self._suburb = suburb
        self._providers = {}
        self._rate = { "monkey" : 5 }

    # @property
    # def centrename(self):
        # return self._centrename

    # @property
    # def is_authenticated(self):
    @property
    def rate(self):
        lenth = 0
        sumrate = 0
        for values in self._rate.values():
            sumrate += int(values)
            lenth += 1
        return sumrate/lenth

    def make_rate(self, name, rate):
        self._rate[name] = rate


    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._centre_type

    @property
    def phone(self):
        return self._phone

    @property
    def abn(self):
        return self._abn

    @property
    def id(self):
        return self._id

    @property
    def suburb(self):
        return self._suburb

    @property
    def providers(self):
        return self._providers

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # @property
    # def admin(self):


    # @admin.setter
    # def admin(self, status):


    def get_id(self):
        """Required by Flask-login"""
        return str(self._id)

    def _generate_id(self):
        Centre.__id += 1
        return Centre.__id

    @classmethod
    def set_id(cls, id):
        cls.__id = id

    # def validate_password(self, password):
    def add_provider(self, provider):
        if self.is_exist(provider.username) == False:
            self._providers[provider.username] = provider

    def is_exist(self, username):
        if username in self.providers:
            return True
        else:
            return False
