import requests, json

def get_key():
    return "iCQXelQA7Dp8cMzWlVJcXB7uKMIhRDprjSmV4ujnLVRpzB2l5yjEqqJULhcKnWKs_te1xT9W_WUWc6omnZQWkK0NLQBqdUpY29BnWoWfmduecgdhotFmO93zFcF1YXYx"
 
def restaurant_search(city):
    key = get_key()

    url = "https://api.yelp.com/v3/businesses/search"
    header = {'Authorization': 'bearer %s' % key}
    params = {
        'location': city
    }

    response = requests.get(url=url, params=params, headers=header)

    data = response.json()

    payload = []

    count = 1
    rest_num = 1
    for restaurant in data["businesses"]:

        rest_data = dict()

        name = data["businesses"][rest_num]["name"]
        try:
            price = data["businesses"][rest_num]["price"]
        except:
            price = False
        try:
            street = data["businesses"][rest_num]["location"]["address1"]
            city = data["businesses"][rest_num]["location"]["city"]
            state = data["businesses"][rest_num]["location"]["state"]
        except:
            street = False

        if price is not False and street is not False:
            rest_data["name"] = name
            rest_data["price"] = price
            rest_data["street"] = street
            rest_data["city"] = city
            rest_data["state"] = state
            count += 1

            payload.append(rest_data)

        rest_num += 1
        if count > 5:
            break

    return json.dumps(payload)