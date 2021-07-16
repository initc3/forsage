#!/usr/bin/env python3

__author__='tyler'

import pandas as pd
import csv

tweet_id_set = set()
user_id_set = set()

count = 0
if __name__ == '__main__':
    with open('twitter_forsage_search_dedup.csv', 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            #print(row.tweet_created_at)
            if row.tweet_id not in tweet_id_set:
                tweet_id_set.add(row.tweet_id)
            else:
                count +=1
            if row.tweet_author_id not in user_id_set:
                user_id_set.add(row.tweet_author_id)

print('Num duplicate tweets: this should be 0: ', count)
print('Number unique tweets: ', len(tweet_id_set))
print('Number unique users: ', len(user_id_set))
print('Avg number tweets/user', (float(len(tweet_id_set))/ len(user_id_set)))
