import csv
from modules.weather import check_weather


class HistoricalData:
    """
    Historical data on where travelers were sent to based on interests
    """
    def __init__(self, file_path):
        self._interest_list = ['Antiques/Flea Markets', 'Architectural Sites', 'Art Galleries', 'Art Museums',
            'Bakeries + Desserts', 'Biking', 'Bookstores', 'Cafes + Coffee Shops', 'Cocktails', 'Comedy Clubs',
            'Craft Beer', 'Dive Bars', 'Family Activities', 'Fine Dining', 'Food Markets', 'Hiking',
            'Historic Sites', 'History Museums', 'Hole-In-The-Wall Restaurants', 'Kayaking', 'LGBTQIA+ Owned Businesses',
            'Live Music', 'Local Boutiques', 'Musical Theater', 'Night Clubs', 'Parks + Gardens', 'Plays',
            'Public + Street Art', 'Quirky Attractions + Oddities', 'Restaurants for Foodies', 'Sailing/Boats',
            'Science Museums', 'Spas', 'Spectator Sports (MLB, NHL, etc.)', 'Thrift Stores', 'Wine', 'Zoos/Aquariums']

        self.city_count_stats = dict()
        self._interest_key = dict()
        self._interest_match = dict()
        self._choices = []

        for num in range(len(self._interest_list)):
            self._interest_key[self._interest_list[num]] = num

        self.import_data(file_path)

    def city_count(self, trip_ids):
        """
        Generate dictionary with city names as keys, and value pair equal to how many times that city has been visited
        """
        total = 0

        for trip in trip_ids:
            city = trip_ids[trip][0]
            if city not in self.city_count_stats:  # city name
                self.city_count_stats[city] = 1
            else:
                self.city_count_stats[city] += 1
            total += 1

        print(self.city_count_stats)
        print(total)
        for city in self.city_count_stats:
            self.city_count_stats[city] = round(self.city_count_stats[city] / total * 100, 2)
        return

    def get_interests(self):
        """
        Getter method used to display interest on input page
        """
        return self._interest_list

    def import_data(self, file_path):
        """
        Read city names and interests from .csv file
        Generate a key that can be used to match interests.
        """
        file = open(file_path)
        csv_f = csv.reader(file)
        next(csv_f)

        # Create dictionary to link city names and list of activities
        trip_ids = dict()
        for row in csv_f:
            if str(row[0]) not in trip_ids:
                trip_ids[str(row[0])] = [
                    row[2],
                    row[4],
                    []
                ]

            trip_ids[str(row[0])][2].append(row[5])

        for trips in trip_ids:
            key = self.generate_interest_key(trip_ids[trips][2])
            self._choices.append(key)
            self._interest_match[key] = [trip_ids[trips][0], trip_ids[trips][1]]

        self.city_count(trip_ids)  # generate city count used for stats

        return

    def generate_interest_key(self, interests):
        """
        Generate key that will be used to match citiesby interest choice.  Key is a string with length equal to number
        of interests in self._interest_list and each character corresponds to an index in the interest list. When a match
        in the given parameter interest is found, the corresponding character of the key is set to 1

        Example:
            interests = ['Antiquies/Flea Markets', 'Zoos/Aquariums']
            key = 1000000000000000000000001
        """
        key = ["0"] * len(self._interest_list)

        for interest in interests:

            index = int(self._interest_key[interest])
            key[index] = str("1")

        return "".join(key)

    def rank_cities(self, traveler_data):
        """
        traveler_data: list of interests given by form data on input page

        returns: dictionary with keys set to a score from 0-(length of interest list). Each score key contains a list
        of cities that have been matched to this score
        """
        search_key = self.generate_interest_key(traveler_data)

        scores = dict()

        # Score cities in historical data based on how well they match up to search_key
        for key in self._interest_match:
            score = 0
            historical_key = key

            for num in range(len(historical_key)):
                if search_key[num] == historical_key[num]:  # matching interest is found
                    score += 1

            city = self._interest_match[key][0]

            if str(score) not in scores:
                scores[str(score)] = [city]
            else:
                scores[str(score)].append(city)

        # Store and rank/sort scores by value
        score_list = []
        for num in scores:
            score_list.append(int(num))
        score_list.sort()

        return scores, score_list

    def find_match(self, traveler_data):
        """
        traveler_data: list of interests given by form data on input page
        returns: list of 3 cities from historical data that match given traveler_data
        """
        scores, score_list = self.rank_cities(traveler_data)

        stats = dict()

        rank = -1
        cur_city_list = []
        while len(cur_city_list) < 15:  # cities can be eliminated due to weather, use 15 as starting point

            for city in scores[str(score_list[rank])]:  # continue adding rank lists until 15 is met
                if city not in cur_city_list:
                    cur_city_list.append(city)
                    stats[city] = round(score_list[rank] / len(self._interest_list)*100)
            rank -= 1


        city_list = [[],[],[]]
        count = 1

        # If weather is not ideal conditions, do not use city
        for city in cur_city_list:
            weather = check_weather(city, "US", "false", 10)
            if weather is True:
                city_list[0].append(city)
                city_list[1].append(stats[city])
                city_list[2].append(self.city_count_stats[city])
                count += 1

            if count > 3:
                break

        print(city_list)
        return city_list


if __name__ == '__main__':
    data = HistoricalData('data\data.csv')
    trav_dat = ['Hiking']
    data.find_match(trav_dat)

