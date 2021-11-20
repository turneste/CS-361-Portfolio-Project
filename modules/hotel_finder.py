import requests, json

def get_key():
    return "iCQXelQA7Dp8cMzWlVJcXB7uKMIhRDprjSmV4ujnLVRpzB2l5yjEqqJULhcKnWKs_te1xT9W_WUWc6omnZQWkK0NLQBqdUpY29BnWoWfmduecgdhotFmO93zFcF1YXYx"

def hotel_search(city):
    key = get_key()

    url = "https://api.yelp.com/v3/businesses/search"
    header = {'Authorization': 'bearer %s' % key}
    params = {
        'term': 'hotel',
        'location': city
    }

    response = requests.get(url=url, params=params, headers=header)

    data = response.json()

    payload = []

    count = 1
    hotel_num = 1
    for hotel in data["businesses"]:

        hotel_data = dict()

        name = data["businesses"][hotel_num]["name"]
        try:
            price = data["businesses"][hotel_num]["price"]
        except:
            price = False
        try:
            street = data["businesses"][hotel_num]["location"]["address1"]
            city = data["businesses"][hotel_num]["location"]["city"]
            state = data["businesses"][hotel_num]["location"]["state"]
        except:
            street = False

        if price is not False and street is not False:
            hotel_data["name"] = name
            hotel_data["price"] = price
            hotel_data["street"] = street
            hotel_data["city"] = city
            hotel_data["state"] = state
            count += 1

            payload.append(hotel_data)

        hotel_num += 1
        if count > 5:
            break

    return json.dumps(payload)

if __name__ == "__main__":
    print(hotel_search())