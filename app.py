from flask import Flask, render_template, request
from modules.historical_data import HistoricalData
from modules.flight_finder import Flights
from modules.restaurant_finder import restaurant_search
from modules.hotel_finder import hotel_search
import json
from datetime import datetime, timedelta


app = Flask(__name__)
historical_data = HistoricalData('modules\data\data.csv')
flights = Flights()

@app.route('/', methods=['GET'])
def input_page():
    """
    Home page where data is inputted
    """
    data = historical_data.get_interests()
    return render_template('index.html', data=data)


@app.route('/', methods=['POST', 'GET'])
def output_page():
    """
    Display 3 cities that closest match to inputted data.
    Display flight, hotel, and restaurant suggestions.
    Display statistics on why 3 cities were chosen
    """

    input_data = request.form

    # Initialization
    output_data = {
        "cities": None,
        "hotels": None,
        "restaurant": None,
        "flights": None,
        "match_stats": dict(),
        "history_stats": dict(),
    }

    age = input_data['age']

    duration = int(input_data['tripLength'])
    #duration = 10

    depart_date = datetime.strptime(input_data['departDate'], '%Y-%m-%d')

    #depart_date = datetime.datetime(2021, 11, 25)
    return_date = depart_date + timedelta(days=duration)

    depart_date = depart_date.strftime('%Y-%m-%d')
    return_date = return_date.strftime('%Y-%m-%d')


    ############################
    #  Generate city data and stats
    ############################

    interests = input_data.getlist("active")
    cities = historical_data.find_match(interests)
    output_data["cities"] = cities[0]

    for num in range(len(cities)):
        output_data["match_stats"][cities[0][num]] = cities[1][num]
        output_data["history_stats"][cities[0][num]] = cities[2][num]

    ############################
    #  Gather hotel data
    ############################

    hotel_list = dict()

    for city in output_data["cities"]:
        hotel_list[str(city)] = json.loads(hotel_search(city))

    output_data["hotels"] = hotel_list

    ############################
    #  Gather flight data
    ############################

    flight_list = {"depart": dict(), "return": dict()}

    for city in output_data["cities"]:
        flight_list["depart"][str(city)] = flights.flight_search("PIT", city, depart_date, 1)
        flight_list["return"][str(city)] = flights.flight_search(city, "PIT", return_date, 1)


    output_data["flights"] = flight_list

    ############################
    #  Gather restaurant data
    ############################

    restaurant_list = dict()

    for city in output_data["cities"]:
        restaurant_list[str(city)] = json.loads(restaurant_search(city))

    output_data["restaurant"] = restaurant_list

    return render_template('output.html', data=output_data)


if __name__ == '__main__':
    app.run(debug=True)

