def hotel_finder(city):
    hotel_list = dict()
    for num in range(1,6):
        hotel_list[str(num)] = {
            "name": "Hotel "+str(num),
            "price": "price here",
            "location": "location here"
        }
    return hotel_list