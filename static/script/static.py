def city_finder(age, budget):
    print(age, budget)
    stat1 = "Stat 1"
    stat2 = "Stat 2"

    stats = [stat1, stat2]
    cities = ["City 1", "City 2", "City 3"]
    return [cities, stats]

def hotel_finder(city):
    hotel_list = []
    for num in range(1,3):
        hotel_name = " Hotel " + str(num)
        hotel_list.append(hotel_name)
    return hotel_list

def flight_finder(city):
    flight_list = []
    for num in range(1,3):
        flight_name = "Flight " + str(num)
        flight_list.append(flight_name)
    return flight_list

def restaurant_finder(city):
    restaurant_list = []
    for num in range(1,3):
        restaurant_name = "Flight " + str(num)
        restaurant_list.append(restaurant_name)
    return restaurant_list
