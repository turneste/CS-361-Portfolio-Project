from flask import Flask, render_template, url_for, request
from modules.historical_data import HistoricalData
from modules.flight_finder import Flights
from modules.restaurant_finder import restaurant_finder
from modules.hotel_finder import hotel_finder
import os


app = Flask(__name__)
historical_data = HistoricalData()
flights = Flights()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = {
            "cities" : None,
            "hotels" : None,
            "restaurant" : None,
            "flights" : None,
            "stats" : None
        }

        ############################
        #  Generate city data
        ############################

        age = request.form['age']

        interest = []
        all_interest = historical_data.get_interests()

        for num in range(len(all_interest)):
            form_req = request.form.get(all_interest[num])
            if form_req is not None:
                interest.append(form_req)

        cities = historical_data.find_match(interest)

        print(cities)

        budget = 1000

        data["cities"] = cities

        ############################
        #  Gather hotel data
        ############################

        hotel_list = dict()

        for city in data["cities"]:

            hotel_list[str(city)] = hotel_finder(city)
        
        data["hotels"] = hotel_list

        ############################
        #  Gather flight data
        ############################
        from threading import Thread

        flight_list = dict()

        for city in data["cities"]:

            flight_list[str(city)] = flights.flight_finder("PIT", "MSY", "2022-03-06", 1)
        
        data["flights"] = flight_list

        ############################
        #  Gather restaurant data
        ############################

        restaurant_list = dict()

        for city in data["cities"]:

            restaurant_list[str(city)] = restaurant_finder(city)
        
        data["restaurant"] = restaurant_list

        return render_template('output.html', data=data)

    else:
        data = historical_data.get_interests()
        return render_template('index.html', data=data)

#  db.create_all()
#  intialize()



if __name__ == '__main__':
    app.run(debug=True)

