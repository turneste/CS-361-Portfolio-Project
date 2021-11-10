def restaurant_finder(city):
    restaurant_list = dict()
    for num in range(1,6):
        restaurant_list[str(num)] = {
            "name": "Restaurant "+str(num),
            "price": "price here",
            "location": "location here"
        }

    return restaurant_list