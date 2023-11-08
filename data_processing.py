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
        filtered_table = Table(self.name + '_filtered', [])
        for item in self.table:
            if condition(item):
                filtered_table.table.append(item)
        return filtered_table

    def aggregate(self, function, key):
        temp = []
        for item in self.table:
            temp.append(float(item[key]))
        return function(temp)

    def select(self, attributes):
        temp = []
        for item in self.table:
            temp_dict = {}
            for key in item:
                if key in attributes:
                    temp_dict[key] = item[key]
                temp.append(temp_dict)
        return temp

    def __str__(self):
        return self.name + ':' + str(self.table)


# test case for temp
table1 = Table('cities', cities)
table2 = Table('countries', countries)
database = DB()
database.insert(table1)
database.insert(table2)
table3 = table1.join(table2, "country")
database.insert(table3)
selected_table = database.search("cities.join")
x = selected_table.filter(lambda c: c["EU"] == "yes").filter(lambda b: b["coastline"] == "no")
country_list = []
print(f"Min temperature for cities in EU that do not have coastlines.\n"
      f"{x.aggregate(lambda a: min(a), 'temperature')}")
print(f"Max temperature for cities in EU that do not have coastlines.\n"
      f"{x.aggregate(lambda a: max(a), 'temperature')}")
# test case for latitude
# selected_table is the same as the one in the previous test case.
for i in selected_table.table:
    if i["country"] not in country_list:
        country_list.append(i["country"])
print(f"Min latitude for cities in every country.")
for j in country_list:
    temp_list = selected_table.filter(lambda c: c["country"] == j)
    if len(temp_list.table) == 0:
        continue
    print(j)
    print(temp_list.aggregate(lambda a: min(a), 'latitude'))
print()
print(f"Max latitude for cities in every country")
for j in country_list:
    temp_list = selected_table.filter(lambda c: c["country"] == j)
    if len(temp_list.table) == 0:
        continue
    print(j)
    print(temp_list.aggregate(lambda a: max(a), 'latitude'))