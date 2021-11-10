# Author: Steve turner
# Description: Initializes database using .csv file

import collections, csv
from modules.weather import check_weather


class HistoricalData:
    def __init__(self):
        self._interest_list = ['Antiques/Flea Markets', 'Architectural Sites', 'Art Galleries', 'Art Museums',
            'Bakeries + Desserts', 'Biking', 'Bookstores', 'Cafes + Coffee Shops', 'Cocktails', 'Comedy Clubs',
            'Craft Beer', 'Dive Bars', 'Family Activities', 'Fine Dining', 'Food Markets', 'Hiking',
            'Historic Sites', 'History Museums', 'Hole-In-The-Wall Restaurants', 'Kayaking', 'LGBTQIA+ Owned Businesses',
            'Live Music', 'Local Boutiques', 'Musical Theater', 'Night Clubs', 'Parks + Gardens', 'Plays',
            'Public + Street Art', 'Quirky Attractions + Oddities', 'Restaurants for Foodies', 'Sailing/Boats',
            'Science Museums', 'Spas', 'Spectator Sports (MLB, NHL, etc.)', 'Thrift Stores', 'Wine', 'Zoos/Aquariums']
        self._interest_key = dict()
        for num in range(len(self._interest_list)):
            self._interest_key[self._interest_list[num]] = num

        self._interest_match = dict()
        self._choices = []


        self.import_data()

    def get_interests(self):
        return self._interest_list

    def import_data(self):
        """Receive and store information from .csv file"""
        file = open('modules\data\data.csv')
        csv_f = csv.reader(file)
        next(csv_f)

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

    def generate_interest_key(self, interests):
        key = ["0"] * len(self._interest_list)
        for interest in interests:
            index = int(self._interest_key[interest])
            key[index] = str("1")
        return "".join(key)

    def find_match(self, traveler_data):
        key1 = self.generate_interest_key(traveler_data)

        scores = dict()
        max_score = 0
        city = ""
        city_key = ""

        city_stats = dict()

        for key in self._interest_match:
            score = 0

            key2 = key
            for num in range(len(key2)):
                if key1[num] == key2[num]:
                    score += 1

            city = self._interest_match[key][0]
            try:
                scores[str(score)].append(city)
            except:
                scores[str(score)] = [city]

            #  city stats
            try:
                city_stats[city] += 1
            except:
                city_stats[city] = 1
        

        city_stats = collections.OrderedDict(sorted(city_stats.items()))


        score_list = []
        for num in scores:
            score_list.append(int(num))
        score_list.sort()

        rank = -1
        cur_city_list = list(set(scores[str(score_list[rank])]))


        while len(cur_city_list) < 3:
            rank -= 1
            cur_city_list += scores[str(score_list[rank])]
            cur_city_list = list(set(cur_city_list))
        

        city_list = []
        count = 1

        print(cur_city_list)

        for city in cur_city_list:
            print(check_weather(city, "US", "false", 10))
            weather = check_weather(city, "US", "false", 10)
            if weather is True:
                city_list.append(city)
                count += 1
            if count > 3:
                break

        return city_list

if __name__ == '__main__':
    data = HistoricalData()
    trav_dat = ['Hiking']
    data.find_match(trav_dat)

