#!/usr/bin/env python3

__author__="tyler"

import csv
from collections import Counter
import sys

list_of_counters = [Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()]

with open("mydata.csv/part-00000-c5fbaa56-0759-422b-995c-85dc16163452-c000.csv","r") as f:
    csv_reader = csv.reader(f)
    headers = next(csv_reader)
    for line in csv_reader:
        month_year = line[0]
        to_address = line[1]
        count = line[2]

        counter_index = None
        if month_year == "2020-01":
            counter_index = 0
        elif month_year == "2020-02":
            counter_index = 1
        elif month_year == "2020-03":
            counter_index = 2
        elif month_year == "2020-04":
            counter_index = 3
        elif month_year == "2020-05":
            counter_index = 4
        elif month_year == "2020-06":
            counter_index = 5
        elif month_year == "2020-07":
            counter_index = 6
        elif month_year == "2020-08":
            counter_index = 7
        elif month_year == "2020-09":
            counter_index = 8
        elif month_year == "2020-10":
            counter_index = 9
        elif month_year == "2020-11":
            counter_index = 10
        elif month_year == "2020-12":
            counter_index = 11
        elif month_year == "2021-01":
            counter_index = 12
        else:
            raise RuntimeError(str(month_year))
        assert(counter_index is not None)

        list_of_counters[counter_index][str(to_address)] = int(count)


for i in range (0, len(list_of_counters)):
    print()
    print(i)
    counter = list_of_counters[i]
    print(counter.most_common(5))
