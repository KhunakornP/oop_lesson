import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))

class DB:
    def __init__(self):
        self.database = []

    def insert(self, data):
        self.database.append(data)

    def search(self, data_name):
        for data_table in self.database:
            if data_name == data_table.name:
                return data_table
        return None

import copy
class Table:
    def __init__(self, name, table):
        self.name = name
        self.table = table

    def join(self, other, key):
        new_table = Table(self.name + ".join", [])
        for item1 in self.table:
            for item2 in other.table:
                if item1[key] == item2[key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    new_table.table.append(dict1)
        return new_table

    def filter(self, condition):
        filtered_list = []
        for item in self.table:
            if condition(item):
                filtered_list.append(item)
        return filtered_list



# Print the average temperature for all the cities in Italy
temps = []
my_country = 'Italy'
for city in cities:
    if city['country'] == my_country:
        temps.append(float(city['temperature']))
print(sum(temps)/len(temps))  

print()
# Print all cities that are not in the EU and whose average temperatures are below 5.0
# Requires joining cities and countries
import copy
cities_ext = []
for city in cities:
    for country in countries:
        if city['country'] == country['country']:
            dict1 = copy.deepcopy(city)
            dict2 = copy.deepcopy(country)
            dict1.update(dict2)
            cities_ext.append(dict1)
for city in cities_ext:
    if city['EU'] == 'no' and float(city['temperature']) < 5.0:
        print(city)
