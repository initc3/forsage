#!/usr/bin/env python3
import csv
import statistics

g_accounts_set = set()
counter = 0
scam_count = 0

inconsistent_language = 0
forsage_bot_score_list = []
forsage_no_scam_bot_score_list = []

def addBotometerScore(line, thinks_scam: bool, botometer_lang: str):
    global forsage_bot_score_list, forsage_no_scam_bot_score_list, inconsistent_language
    score = 0
    if botometer_lang != '':
        if botometer_lang != 'en':
            forsage_bot_score_list.append(float(line[26]))
            if not thinks_scam:
                forsage_no_scam_bot_score_list.append(float(line[26]))
        else:
            forsage_bot_score_list.append(float(line[19]))
            if not thinks_scam:
                forsage_no_scam_bot_score_list.append(float(line[26]))



with open('../data/twitter_forsage_search_bot_annotated.csv','r') as f:
    csv_reader = csv.reader(f)
    #next(csv_reader)
    for line in csv_reader:
        counter += 1
        tweet_author_id = line[0]
        tweet_message = line[13]
        twitter_lang = line[11]
        botometer_lang = line[14]
        if twitter_lang != botometer_lang:
            inconsistent_language += 1
        thinks_scam = ('scam' in tweet_message.lower() or 'ponzi' in tweet_message.lower())
        if thinks_scam:
            scam_count +=1
        if tweet_author_id not in g_accounts_set:
            g_accounts_set.add(tweet_author_id)
            addBotometerScore(line, thinks_scam, botometer_lang)
        else:
            if not thinks_scam:
                addBotometerScore(line, thinks_scam, botometer_lang)

print('num tweets: ', counter)
print('num unique accounts: ', len(g_accounts_set))

print('mean, median botometer score: ', statistics.mean(forsage_bot_score_list), ' ', statistics.median(forsage_bot_score_list))
print('mean, median botometer not a scam score: ', statistics.mean(forsage_no_scam_bot_score_list), ' ', statistics.median(forsage_no_scam_bot_score_list))
print('number inconsistent_language: ', inconsistent_language)

print('num tweets think scam: ', scam_count)
