def city_finder(age, budget):
    """City matching algorithm"""
    stat1 = "Stat 1"
    stat2 = "Stat 2"







    stats = [stat1, stat2]
    cities = ["City 1", "City 2", "City 3"]
    return [cities, stats]

def hotel_finder(city):
    hotel_list = dict()
    for num in range(1,6):
        hotel_list[str(num)] = {
            "name": "Hotel "+str(num),
            "price": "price here",
            "location": "location here"
        }
    return hotel_list

def flight_finder(city):
    flight_list = dict()
    for num in range(1,6):
        flight_list[str(num)] = {
            "name": "Flight "+str(num),
            "price": "price here",
            "location": "location here"
        }
    return flight_list

def restaurant_finder(city):
    restaurant_list = dict()
    for num in range(1,6):
        restaurant_list[str(num)] = {
            "name": "Restaurant "+str(num),
            "price": "price here",
            "location": "location here"
        }

    return restaurant_list

