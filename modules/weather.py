import json, urllib.request
import requests


def check_weather(city, country, outdoor, duration):
    return True

    base_url = "http://flip3.engr.oregonstate.edu:44643/getWeather?"
    city_query = "city=" + city
    country_query = "&country=" + country
    outdoor_query = "&outdoorFlag=" + outdoor

    url = base_url + city_query + country_query + outdoor_query

    try:
        data = requests.get(url=url, timeout=1)
        weather = data.json()
    except:
        print("timeout")
        return True
    
    for day in range(1, duration):
        trip_feas = weather["days"][str(day)]["tripFeasibility"]
        activ_feas = weather["days"][str(day)]["activityFeasible"]

        if trip_feas == "false":
            return False

        if outdoor is True:
            if activ_feas == "false":
                return False
    return True


if __name__ == "__main__":
    print(check_weather("San Luis Obispo", "US", "false", 10))
