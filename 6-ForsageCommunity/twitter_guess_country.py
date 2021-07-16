#!/usr/bin/env python3

__author__='tyler'

import csv
import geograpy
import pycountry
import sys


g_accounts_done = {}

g_accounts_w_geos = {}
linecount = 0

with open('twitter2/twitter_forsage_search_dedup.csv','r') as f:
    csv_reader = csv.reader(f)
    print(next(csv_reader))
    for line in csv_reader:
        linecount += 1
        tweet_author_id = line[0]
        twitter_geo = line[4]
        if twitter_geo != '':
            if twitter_geo != 'nan':
                print(tweet_author_id, twitter_geo)
                g_accounts_w_geos[tweet_author_id] = twitter_geo


print(len(g_accounts_w_geos))
print(linecount)

with open('../data/twitter_accounts_geo_iso.csv','r') as old_twitter_file:
    csv_reader = csv.reader(old_twitter_file)
    for line in csv_reader:
        assert len(line) == 3 , '{} != 3'.format(len(line))
        tweet_author_id = line[0]
        iso_location = line[1]
        twitter_geo = line[2]
        g_accounts_done[tweet_author_id] = (iso_location, twitter_geo)



with open('../data/twitter_accounts_geo_iso-fail2.csv','w') as fail_file:
    fail_writer = csv.writer(fail_file)
    with open('../data/twitter_accounts_geo_iso2.csv','w') as out_file:
        csv_writer = csv.writer(out_file)
        for tweet_author_id, twitter_geo in g_accounts_w_geos.items():
            if tweet_author_id in g_accounts_done:
                print('FOUND ALREADY HAND-FINISHED ACCOUNT, SKIPPING')
                continue
            print(twitter_geo)
            places = geograpy.get_geoPlace_context(text=twitter_geo)
            if len(places.countries) == 0:
                fail_writer.writerow([tweet_author_id, twitter_geo])
                continue
            p_country = pycountry.countries.get(name=places.countries[0])
            iso_code = p_country.alpha_3
            print(iso_code)
            out_line = [tweet_author_id, iso_code, twitter_geo]
            csv_writer.writerow(out_line)




