#!/usr/bin/env python3

import csv
import json
import numpy as np
from iso3166 import countries

g_channel_dict = {}
g_num_totalvideos = 0
g_country_dict = {}

viewcount_list = []

with open('../data/youtube_forsage_search.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for ( video_title, video_id, video_view_count, video_published_at, video_description,
            channel_title, channel_id, channel_sum_view_count, channel_published_at,
            channel_sum_video_count, channel_subscriber_count,
            channel_country, channel_description) in csv_reader:
        g_num_totalvideos += 1
        #print(video_title)
        channel_stat = g_channel_dict.pop(channel_id, None)
        number_videos_about_forsage = 0
        viewcount_list.append(video_view_count)
        if channel_stat is None:
            channel_stat = [channel_title, channel_sum_view_count, channel_published_at, channel_sum_video_count, channel_subscriber_count, channel_country, channel_description, number_videos_about_forsage]
        # paranoia check
        if (channel_stat[0] != channel_title
            or channel_stat[1] != channel_sum_view_count
            or channel_stat[2] != channel_published_at
            or channel_stat[3] != channel_sum_video_count
            or channel_stat[4] != channel_subscriber_count
            or channel_stat[5] != channel_country
            or channel_stat[6] != channel_description
        ):
            #raise Exception("Error in the data? {} | {}".format(channel_title, channel_stat[0]))
            print("Error data not match even though channel Ids match:")
            #print("{} {} | {} {} | {} {} | {} {} | {} {} | {} {} | {} {}".format(
            print("{} {} | {} {} | {} {} | {} {} | {} {} | {} {}".format(
                channel_title, channel_stat[0],
                channel_sum_view_count, channel_stat[1],
                channel_published_at, channel_stat[2],
                channel_sum_video_count, channel_stat[3],
                channel_subscriber_count, channel_stat[4],
                channel_country, channel_stat[5]
                #channel_description, channel_stat[6],
            ))
        number_videos_about_forsage = channel_stat[7] + 1
        g_channel_dict[channel_id] = channel_stat

for (_, channel) in g_channel_dict.items():
    country = channel[5]
    if country:
        country_long = countries.get(country).name
    else:
        country_long = ""
    country_count = g_country_dict.get(country, 0)
    country_count += 1
    g_country_dict[country] = country_count

print("Number of total videos: ", g_num_totalvideos)
print("Number of total unique channels: ", len(g_channel_dict))

top_cutoff = np.percentile(viewcount_list, 97, interpolation='nearest')
print(top_cutoff)
above_cutoff = 0
with open('../data/youtube_forsage_search.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for ( video_title, video_id, video_view_count, video_published_at, video_description,
            channel_title, channel_id, channel_sum_view_count, channel_published_at,
            channel_sum_video_count, channel_subscriber_count,
            channel_country, channel_description) in csv_reader:
        if video_view_count >= top_cutoff:
            above_cutoff += 1
            print(video_title)
            print(video_view_count)

print('Total videos above the 97th percentile: ', str(above_cutoff))


# print("Country breakdown: ")
# print(json.dumps(g_country_dict, sort_keys=True, indent=4))
