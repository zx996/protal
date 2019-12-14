from flask import Flask
from flask_login import LoginManager
from lib.dao.user_dao import UserManager
from lib.dao.provider_dao import CentreManager
from lib.health_data import HealthData


app = Flask(__name__)
app.secret_key = 'very-secret-123'  # Used to add entropy
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Loads data
#centremanager = CentreManager.load_data()
#user_db = UserManager.load_data()
user_db, centremanager = HealthData.load_data()
