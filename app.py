from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import static.script.static as static

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Travel_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    city_depart = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    interest = db.Column(db.Integer, nullable=False)  # list

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
        #  Generate restaurant data
        ############################


        age = request.form['age']
        budget = 1000
        search_data = static.city_finder(age, budget)

        data["cities"] = search_data[0]
        data["stats"] = search_data[1]

        ############################
        #  Gather hotel data
        ############################

        hotel_list = dict()

        for city in data["cities"]:

            hotel_list[str(city)] = (static.hotel_finder(city))
        
        data["hotels"] = hotel_list

        ############################
        #  Gather flight data
        ############################

        flight_list = dict()

        for city in data["cities"]:

            flight_list[str(city)] = (static.flight_finder(city))
        
        data["flights"] = flight_list

        ############################
        #  Gather restaurant data
        ############################

        restaurant_list = dict()

        for city in data["cities"]:

            restaurant_list[str(city)] = (static.restaurant_finder(city))
        
        data["restaurant"] = restaurant_list



        return render_template('output.html', data=data)

    else:
        return render_template('index.html')

#  db.create_all()
#  intialize()



if __name__ == '__main__':
    app.run(debug=True)

