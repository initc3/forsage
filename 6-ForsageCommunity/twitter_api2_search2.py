#!/usr/bin/env python3

import requests
import json
import csv
import sys
import time
import traceback

g_users_dict = {}
NEXT_TOKEN = ''
counter = 0
total_tweets_written = 0

def parseResponse(sample,csv_writer):
    global total_tweets_written
    tweet_dict = {}
    tweet_author_dict = {}
    final_dict = {}
    print('Sample data length: {}'.format(len(sample['data'])))
    for data in sample['data']:
        tweet_author_id = data.get('author_id', '')
        tweet_conversation_id = data.get('conversation_id', '')
        tweet_created_at = data.get('created_at', '')
        tweet_id = data.get('id', '')
        tweet_text = data.get('text', '')
        tweet_lang = data.get('lang', '')
        tweet_geo = data.get('geo', '')

        tweet_dict[tweet_id] = [ tweet_conversation_id, tweet_created_at, tweet_id, tweet_lang, tweet_geo, tweet_text ]

        this_authors_tweets = tweet_author_dict.get(tweet_author_id, None)
        if this_authors_tweets:
            this_authors_tweets = this_authors_tweets + [ tweet_id ]
        else:
            this_authors_tweets = [ tweet_id ]
        tweet_author_dict[tweet_author_id] = this_authors_tweets

    for users in sample['includes']['users']:
        tweet_author_id = users['id']
        tweet_author_add_info = ['','','','', '']
        if tweet_author_id not in g_users_dict:
            for _ in range(0,2):
                try:
                    r2 = requests.get('https://api.twitter.com/2/users?ids={}&user.fields=created_at,verified,public_metrics,url,location'.format(tweet_author_id), headers=hdrs)
                    r2.raise_for_status()
                    break
                except:
                    track = traceback.format_exc()
                    print(track)
                    print("Got exception2 while trying to make query. probably rate-limiting. Waiting 15 minutes.")
                    time.sleep(15*60+1)
            user_info_json = r2.json()
            for data2 in user_info_json['data']:
                author_location = data2.get('location','')
                author_verified = data2.get('verified','')
                author_created_at = data2.get('created_at','')
                author_url = data2.get('url')
                public_metrics = data2.get('public_metrics',None)
                if public_metrics:
                    author_followers_count = public_metrics.get('followers_count','')
                else:
                    author_followers_count = ''
            tweet_author_add_info = [ author_created_at, author_location, author_verified, author_url, author_followers_count ]
            g_users_dict[tweet_author_id] = tweet_author_add_info
        else:
            tweet_author_add_info = g_users_dict.get(tweet_author_id)
        this_authors_tweets = tweet_author_dict[tweet_author_id]
        for tweet_id in this_authors_tweets:
            tweet_data = tweet_dict[tweet_id]
            author_name = users.get('name', '')
            author_username = users.get('username','')
            all_data = [tweet_author_id, author_name, author_username] + tweet_author_add_info + tweet_data
            final_dict[tweet_id] = all_data
    counter2 = 0
    for _,tweet_data_row in final_dict.items():
        # tweet_author_id, author_name, author_username, author_created_at, author_location, author_verified, author_url, author_followers_count, tweet_conversation_id, tweet_created_at, tweet_id, tweet_lang, tweet_geo, tweet_text
        csv_writer.writerow(tweet_data_row)
        counter2 += 1
    total_tweets_written += counter2
    print("Wrote Rows: {}".format(counter2))


with open("../apikeys/twitter_api_bearer_token_tyler.txt", "r") as f:
    bearer_token = f.read().strip()
    hdrs = {'Authorization': 'Bearer ' + bearer_token}

with open('../data/twitter_forsage_search.csv', 'a') as csv_file:
    csv_writer = csv.writer(csv_file)
    while total_tweets_written < 100000:
        print('Request {} {} {}'.format(counter, total_tweets_written, NEXT_TOKEN))
        if NEXT_TOKEN:
            r = requests.get('https://api.twitter.com/2/tweets/search/recent?query=forsage&max_results=100&tweet.fields=created_at,lang,conversation_id,geo&expansions=author_id,geo.place_id&next_token={}'.format(NEXT_TOKEN), headers=hdrs)
        else:
            r = requests.get('https://api.twitter.com/2/tweets/search/recent?query=forsage&max_results=100&tweet.fields=created_at,lang,conversation_id,geo&expansions=author_id,geo.place_id', headers=hdrs)
        try:
            r.raise_for_status()
            response_sample = r.json()
            parseResponse(response_sample, csv_writer)
            counter += 1
            NEXT_TOKEN = response_sample['meta']['next_token']
        except:
            track = traceback.format_exc()
            print(track)
            print("Got exception while trying to make query. probably rate-limiting. Waiting 15 minutes.")
            time.sleep(15 * 60 + 1)
