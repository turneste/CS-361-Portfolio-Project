from amadeus import Client
from amadeus import Location
import json


class Flights:
    def __init__(self):
        """
        -Create dictionary for converting iata codes to airline names
        -amadeus class is a Python library for Amadeus API calls
        """
        self._iata_dict = self.import_data()
        self.amadeus = Client(
            client_id='2jYFWy2lwS0uSozHuSAng4AoW2MegMM2',
            client_secret='5Vcc9CKogcI39b7N'
        )

    def import_data(self):
        """
        Convert iata json file to readable format
        """
        file = open("modules\data\iata.json")
        data = json.load(file)
        return data

    def find_iata_by_city(self, city):
        """
        city: Any city in the United States
        returns: Iata code for largest airport
        """
        response = self.amadeus.reference_data.locations.get(keyword=city, subType=Location.ANY)
        return response.data[0]["iataCode"]

    def flight_data_format(self, flight_search_data):
        """
        flight_search_data: All possible flight options returned by flight search
        returns: 3 flight options in format output_page() is expecting
        """
        count = 1
        flight_list = dict()

        for flight in flight_search_data:  # iterate through flight options until 3 are found

            # Connecting flight information
            segments = []
            for segment in flight["itineraries"][0]["segments"]:

                # Convert iata code given by flight_search() to airline names
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

    def flight_search(self, depart_city, dest_city, date, adults=1):
        """
        depart_city: City traveler is departing from
        dest_city: City traveler is departing to
        date: Departure date
        adults: Number of travelers
        """

        # Find iata code from city name, required for amadeus search
        dept_code = self.find_iata_by_city(depart_city)
        dest_code = self.find_iata_by_city(dest_city)

        response = self.amadeus.shopping.flight_offers_search.get(
            originLocationCode=dept_code,
            destinationLocationCode=dest_code,
            departureDate=date,
            adults=1,
            max=3,
            currencyCode='USD',
            )

        data = response.data

        flight_list = self.flight_data_format(data)

        return flight_list

if __name__ == "__main__":
    flights = Flights()
    print(flights.flight_search("PIT", "MSY", "2022-03-06", 1))
