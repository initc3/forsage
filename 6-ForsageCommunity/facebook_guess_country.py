#!/usr/bin/env python3

__author__='tyler'

import csv
import geograpy
import pycountry
import sys


with open('./forsageinformationgroup-withloc-iso-fail.csv','w') as fail_file:
    fail_writer = csv.writer(fail_file)
    with open('./forsageinformationgroup-withloc-iso.csv','w') as out_file:
        csv_writer = csv.writer(out_file)
        with open('./forsageinformationgroup-withloc.csv','r') as in_file:
            csv_reader = csv.reader(in_file)
            for line in csv_reader:
                print(line)
                places = geograpy.get_geoPlace_context(text=line[3])
                if len(places.countries) == 0:
                    fail_writer.writerow(line)
                    continue
                p_country = pycountry.countries.get(name=places.countries[0])
                iso_code = p_country.alpha_3
                print(iso_code)
                out_line = line + [iso_code]
                csv_writer.writerow(out_line)


