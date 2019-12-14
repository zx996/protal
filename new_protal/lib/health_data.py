from lib.dao.user_dao import UserManager
from lib.dao.provider_dao import CentreManager
from lib.user import *
from lib.centre import *
from lib.appointment import *
import csv


class HealthData:
    @classmethod
    def load_data(cls):

        centremanager = CentreManager()
        user_db = UserManager()

        with open("csv/patient.csv", "r") as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                username = row[0]
                password = row[1]
                # GIAN EDIT
                fullname = row[2]
                phone = row[3]
                #-----------
                admin = False
                dev = Patient(username, password,fullname,phone)
                user_db.add_user(dev)

        with open("csv/provider.csv", "r") as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                username = row[0]
                password = row[2]
                service = row[1]
                # GIAN EDIT
                fullname = row[3]
                phone = row[4]
                #-----------
                centre = "individual"
                dev = Provider(username, password, centre, service, fullname, phone)
                user_db.add_user(dev)
                centremanager.add_provider(dev)

        with open("csv/health_centres.csv", "r") as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
    			#add centre to  centremanager
                centre_type = row[0]
                abn = row[1]
                name_centre = row[2]
                phone = row[3]
                suburb = row[4]
                dev = Centre(centre_type, abn, name_centre, phone, suburb)
                centremanager.add_centre(dev)

        with open("csv/provider_health_centre.csv", "r") as health:
            provider_at_centre = csv.reader(health)
            for row in provider_at_centre:
                username = row[0]
                centre = row[1] 
                start = row[2]      
                end = row[3]
                provider = centremanager.get_provider(username)
                provider.add_workhour(centre,start,end)

                centremanager.add_provider_centre(centre, username)

        with open("csv/specialist.csv", "r") as health:
            specialist = csv.reader(health)
            for row in specialist:
                username = row[0]
                password = row[1]
                centre = None
                service = row[2]
                fullname = row[3]
                phone = row[4]
                dev = Specialist(username, password, centre, service, fullname, phone)
                user_db.add_user(dev)
                centremanager.add_provider(dev)
        return user_db, centremanager
