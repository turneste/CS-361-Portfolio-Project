import requests, json, csv

from requests.api import get

class Flights:
    def __init__(self):
        self._token = self.get_token()

    def get_token(self):
        base_url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        params = {
            "grant_type": "client_credentials",
            "client_id": "2jYFWy2lwS0uSozHuSAng4AoW2MegMM2",
            "client_secret": "5Vcc9CKogcI39b7N"
        }

        header = {"Content-Type" : "application/x-www-form-urlencoded"}
        response = requests.post(base_url, data=params, headers=header)
        data = response.json()
        return data["access_token"]

    def flight_finder(self):

        url = "https://test.api.amadeus.com/v3/shopping/hotel-offers?"

        try:
            header = {"Authorization": "Bearer " + self._token}
        except:
            self._token = self.get_token()
            header = {"Authorization": "Bearer " + self._token}

        params = {
            "hotelIds":"HLLON101",
            "adults":1,
            "checkInDate": "2022-06-20"
        }

        response = requests.get(url, params=params, headers=header)

        data = response.json()
        print(data)

 
        return

if __name__ == "__main__":
    flights = Flights()
    flights.flight_finder()