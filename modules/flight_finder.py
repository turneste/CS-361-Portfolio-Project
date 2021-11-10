import requests, json, csv

from requests.api import get

class Flights:
    def __init__(self):
        self._token = self.get_token()
        self._iata_dict = self.import_data()

    def import_data(self):
        file = open("modules\data\iata.json")
        data = json.load(file)
        return data

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

    def flight_finder(self, departCity, destCity, date, adults=1):

        departCode = departCity
        arriveCode = destCity
        departDate = date
        adults = adults

        #key = get_token()

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers?"

        try:
            header = {"Authorization": "Bearer " + self._token}
            print(header)
        except:
            self._token = self.get_token()
            header = {"Authorization": "Bearer " + self._token}

        params = {
            "originLocationCode": departCode,
            "destinationLocationCode": arriveCode,
            "departureDate": departDate,
            "adults": 1,
            "currencyCode": "USD",
            "max": 5,
            "includedAirlineCodes": "UA"
        }

        response = requests.get(url, params=params, headers=header)

        data = response.json()

        count = 1
        flight_list = dict()
        for flight in data["data"]:

            segments = []
            for segment in flight["itineraries"][0]["segments"]:
                depCity = segment["departure"]["iataCode"]
                arrCity = segment["arrival"]["iataCode"]
                airline = segment["carrierCode"]
                airline_name = self._iata_dict[airline]
                segments.append({
                    "depCity": depCity,
                    "arrCity": arrCity,
                    "airline": airline_name
                })

            price = flight["price"]["grandTotal"]

            flight_list[str(count)] = {
                "price": price,
                "segments": segments
            }

            count += 1
            if count > 4:
                break

        print(flight_list)
        return flight_list

if __name__ == "__main__":
    flights = Flights()
    flights.flight_finder("PIT", "MSY", "2022-03-06", 1)
