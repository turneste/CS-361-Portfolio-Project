# Author: Steve turner
# Description: Initializes database using .csv file

from flask_sqlalchemy import SQLAlchemy
from app import db, Travel_Data


def import_data():
    """Receive and store information from .csv file"""
    pass

def clean_data():
    """Sort and transform data to be usable in application"""
    pass


def intialize():  # Will receive data from .csv
    """Store data in database"""
    traveler_data = Travel_Data(age=55, city_depart="Pittsburgh", budget=3000, interest="Hiking")
    db.session.add(traveler_data)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    intialize()
