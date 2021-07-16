#!/usr/bin/env python3

import csv
import pycountry
import json

gender_male_count = 0
gender_female_count = 0
gender_unspecified_count = 0

location_unspecified_count = 0
countries_dict = {}

with open("forsageinformationgroup.csv","r") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        gender = row[2]
        if gender == "Male":
            gender_male_count += 1
        elif gender == "Female":
            gender_female_count += 1
        else:
            gender_unspecified_count += 1

with open("forsageinformationgroup2.csv","r") as f2:
    csvreader = csv.reader(f2)
    for row in csvreader:
        locationstring = row[3]
        if locationstring == "":
            location_unspecified_count += 1
        else:
            found = False
            for country in pycountry.countries:
                if country.name in locationstring:
                    if country.name == "Niger": # special niger/nigeria case
                        if "Nigeria" in locationstring:
                            continue
                    found = True
                    countries_dict[country.name] = countries_dict.get(country.name, 0) + 1
            if not found:
                print("Couldn't parse country string, giving up")
                print(locationstring)


print("Num Male: ", gender_male_count)
print("Num Female: ", gender_female_count)
print("Unspecified: ", gender_unspecified_count)
print("Of specified: gender ratio: {:.2%} M  {:.2%} F".format((gender_male_count/ (gender_male_count+gender_female_count)), (gender_female_count / (gender_female_count + gender_male_count)) ))
print("Countries", json.dumps(countries_dict, sort_keys=True, indent=4))
