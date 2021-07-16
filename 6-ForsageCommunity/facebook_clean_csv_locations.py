#!/usr/bin/env python3

import csv
import pycountry
import re

regexes = [ re.compile("Places Lived"), re.compile("Current City"), re.compile("Hometown"), re.compile("Moved in [0-9][0-9][0-9][0-9]"), re.compile("Moved here") ]

count_location_unspecified = 0

with open("forsageinformationgroup2.csv","w") as f2:
    csv_writer = csv.writer(f2)
    with open("forsageinformationgroup.csv","r") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            if line[3] != '':
                addr_field = line[3]
                addr = addr_field
                for regex in regexes:
                    addr = re.sub(regex, " ", addr)
                addr = addr.strip()
                print(addr)
                new_row = [line[0], line[1], line[2], addr]
                csv_writer.writerow(new_row)
                # found = False
                # first_found_country = ''
                # first_found_country_index = 1000
                # for country in pycountry.countries:
                #     country_start = addr.find(country.name)
                #     if country_start != -1 and not found:
                #         if country.name == "Niger": # special niger/nigeria case
                #             if "Nigeria" in addr:
                #                 continue
                #         found = True
                #         first_found_country = country
                #         first_found_country_index = country_start
                #     elif country_start != -1 and found:
                #         if country.name == "Niger": # special niger/nigeria case
                #             if "Nigeria" in addr:
                #                 continue
                #         if country_start < first_found_country_index:

            # else:
            #    count_location_unspecified += 1


