import pickle
from abc import ABC, abstractmethod
from lib.appointment import Appointment
from lib.user import *


class UserDAO(ABC):
    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def validate_login(self, username, password):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def is_exist(self, username):
        pass

    @abstractmethod
    def max_id(self):
        pass

    @abstractmethod
    def get_patient(self):
        pass

    def save_data(self):
        pass

    @classmethod
    @abstractmethod
    def load_data(cls):
        pass


class UserManager(UserDAO):
    def __init__(self):
        self._users = {}

    def add_user(self, user):
        if self.is_exist(user.username) == False:
                self._users[user.username] = user

    def validate_login(self, username, password):
        user = self._users.get(username)
        if user is None:
            return None
        return user if user.validate_password(password) else None

    def find_by_id(self, id):
        for i in self._users.values():
            if i.get_id() == id:
                return i
        # Not necessary but explicit
        return None

    def get_patient(self, name):
        for values in self._users.values():
            if values.username == name and values.__class__.__name__ == "Patient":
                return values
        # Not necessary but explicit
        return None

    def is_exist(self, username):
        if username in self._users:
            return True
        else:
            return False

    def max_id(self):
        return max([int(x.get_id()) for x in self._users.values()])

    def save_data(self):
        with open('users.dat', 'wb') as file:
            pickle.dump(self, file)

    @property
    def show_user(self):
        return self._users


    @classmethod
    def load_data(cls):
        try:
            with open('users.dat', 'rb') as file:
                user_db = pickle.load(file)
            file.close()
            User.set_id(user_db.max_id())
        except IOError:
            user_db = UserManager()
        return user_db
