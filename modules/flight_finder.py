from amadeus import Client, ResponseError
from amadeus import Location
import csv, json, time

class Flights:
    def __init__(self):
        self._iata_dict = self.import_data()
        self.amadeus = Client(
            client_id='2jYFWy2lwS0uSozHuSAng4AoW2MegMM2',
            client_secret='5Vcc9CKogcI39b7N'
        )

    def import_data(self):
        file = open("modules\data\iata.json")
        data = json.load(file)
        return data

    def find_iata_by_city(self, city):
        response = self.amadeus.reference_data.locations.get(keyword=city, subType=Location.ANY)
        return response.data[0]["iataCode"]

    def flight_data_format(self, data):
        count = 1
        flight_list = dict()
        for flight in data:

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
                "segments": segments,
                "airline_name": airline_name
            }

            count += 1
            if count > 4:
                break

        return flight_list


    def flight_search(self, departCity, destCity, date, adults=1):

        start = time.perf_counter()

        deptCode = self.find_iata_by_city(departCity)
        destCode = self.find_iata_by_city(destCity)
        departDate = date
        adults = adults

        response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode = deptCode,
            destinationLocationCode = destCode,
            departureDate=departDate,
            adults=1,
            max = 3,
            currencyCode = 'USD',
            )

        data = response.data
        print(data)

        end = time.perf_counter()
        print("Time elapsed:", end-start)

        flight_list = self.flight_data_format(data)

        return flight_list

if __name__ == "__main__":
    flights = Flights()
    print(flights.flight_search("PIT", "MSY", "2022-03-06", 1))
