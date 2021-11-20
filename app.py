from flask import Flask, render_template, url_for, request
from modules.historical_data import HistoricalData
from modules.flight_finder import Flights
from modules.restaurant_finder import restaurant_search
from modules.hotel_finder import hotel_search
import os, datetime, json


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

        age = request.form['age']

        duration = request.form['triplength']
        #duration = 10

        depart_date = datetime.strptime(request.form['departDate'], '%Y %m %d')

        #depart_date = datetime.datetime(2021, 11, 25)
        return_date = depart_date + datetime.timedelta(days=duration)
 
        depart_date = depart_date.strftime('%Y-%m-%d')
        return_date = return_date.strftime('%Y-%m-%d')
        

        ############################
        #  Generate city data
        ############################

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

            hotel_list[str(city)] = json.loads(hotel_search(city))
        
        data["hotels"] = hotel_list

        ############################
        #  Gather flight data
        ############################
        from threading import Thread

        flight_list = {"depart":dict(), "return":dict()}

        for city in data["cities"]:

            flight_list["depart"][str(city)] = flights.flight_search("PIT", city, depart_date, 1)
            flight_list["return"][str(city)] = flights.flight_search(city, "PIT", return_date, 1)

            # stop calls to debug
            """
            flight_list["depart"][str(city)] = {"1":{"airline_name":"debug", "price":"debug"}}
            flight_list["return"][str(city)] = {"1":{"airline_name":"debug", "price":"debug"}}
            """
        
        print(flight_list)
        data["flights"] = flight_list

        ############################
        #  Gather restaurant data
        ############################

        restaurant_list = dict()

        for city in data["cities"]:

            restaurant_list[str(city)] = json.loads(restaurant_search(city))
        
        data["restaurant"] = restaurant_list

        return render_template('output.html', data=data)

    else:
        data = historical_data.get_interests()
        return render_template('index.html', data=data)

#  db.create_all()
#  intialize()



if __name__ == '__main__':
    app.run(debug=True)

