import botometer
import sys
import csv
from ratelimit import limits, sleep_and_retry

twitter_consumer_key = 'lala'
twitter_consumer_secret = 'lala'
rapidapi_key = 'lala'
twitter_app_auth = {
    'consumer_key': twitter_consumer_key,
    'consumer_secret': twitter_consumer_secret,
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


TWENTY_FOUR_HOURS = (24 * 60 * 60)
@sleep_and_retry
@limits(calls=2000, period=TWENTY_FOUR_HOURS)
def do_bombom(tweet_author_id):
    return bom.check_account(tweet_author_id)

g_already_finished_tweets_set = set()
g_users_dict = {}
with open('twitter_forsage_search_bot_annotated.csv','r') as bot_in_file:
    csv_reader = csv.reader(bot_in_file)
    for line in csv_reader:
        tweet_author_id = line[0]
        majority_lang = line[14]
        raw_scores_eng_astroturf = line[15]
        raw_scores_eng_fake_follower = line[16]
        raw_scores_eng_financial = line[17]
        raw_scores_eng_other = line[18]
        raw_scores_eng_overall = line[19]
        raw_scores_eng_self_declared = line[20]
        raw_scores_eng_spammer = line[21]

        raw_scores_uni_astroturf = line[22]
        raw_scores_uni_fake_follower = line[23]
        raw_scores_uni_financial = line[24]
        raw_scores_uni_other = line[25]
        raw_scores_uni_overall = line[26]
        raw_scores_uni_self_declared = line[27]
        raw_scores_uni_spammer = line[28]
        bot_score = [ majority_lang, raw_scores_eng_astroturf, raw_scores_eng_fake_follower, raw_scores_eng_financial, raw_scores_eng_other, raw_scores_eng_overall, raw_scores_eng_self_declared, raw_scores_eng_spammer, raw_scores_uni_astroturf, raw_scores_uni_fake_follower, raw_scores_uni_financial, raw_scores_uni_other, raw_scores_uni_overall, raw_scores_uni_self_declared, raw_scores_uni_spammer ]
        g_users_dict[tweet_author_id] = bot_score

with open('twitter_forsage_search_NEW_bot_annotated.csv','r') as bot_in_file2:
    csv_reader = csv.reader(bot_in_file2)
    for line in csv_reader:
        tweet_author_id = line[0]
        majority_lang = line[14]
        raw_scores_eng_astroturf = line[15]
        raw_scores_eng_fake_follower = line[16]
        raw_scores_eng_financial = line[17]
        raw_scores_eng_other = line[18]
        raw_scores_eng_overall = line[19]
        raw_scores_eng_self_declared = line[20]
        raw_scores_eng_spammer = line[21]

        raw_scores_uni_astroturf = line[22]
        raw_scores_uni_fake_follower = line[23]
        raw_scores_uni_financial = line[24]
        raw_scores_uni_other = line[25]
        raw_scores_uni_overall = line[26]
        raw_scores_uni_self_declared = line[27]
        raw_scores_uni_spammer = line[28]
        bot_score = [ majority_lang, raw_scores_eng_astroturf, raw_scores_eng_fake_follower, raw_scores_eng_financial, raw_scores_eng_other, raw_scores_eng_overall, raw_scores_eng_self_declared, raw_scores_eng_spammer, raw_scores_uni_astroturf, raw_scores_uni_fake_follower, raw_scores_uni_financial, raw_scores_uni_other, raw_scores_uni_overall, raw_scores_uni_self_declared, raw_scores_uni_spammer ]
        g_users_dict[tweet_author_id] = bot_score

        tweet_id = line[10]
        g_already_finished_tweets_set.add(tweet_id)




print('imported old g_users_dict of len ', len(g_users_dict))
print('imported already_finished of len ', len(g_already_finished_tweets_set))

with open('twitter_forsage_search_dedup.csv','r') as f:
    with open('twitter_forsage_search_NEW_bot_annotated.csv','a') as f2:
        csv_reader = csv.reader(f)
        old_header = next(csv_reader)
        csv_writer = csv.writer(f2)
        header_bot_score = [ 'majority_lang', 'raw_scores_eng_astroturf', 'raw_scores_eng_fake_follower', 'raw_scores_eng_financial', 'raw_scores_eng_other', 'raw_scores_eng_overall', 'raw_scores_eng_self_declared', 'raw_scores_eng_spammer', 'raw_scores_uni_astroturf', 'raw_scores_uni_fake_follower', 'raw_scores_uni_financial', 'raw_scores_uni_other', 'raw_scores_uni_overall', 'raw_scores_uni_self_declared', 'raw_scores_uni_spammer' ]
        #csv_writer.writerow(old_header + header_bot_score)
        for line in csv_reader:
            tweet_author_id = line[0]
            print(line)
            bot_score = ['','','','','','','','','','','','','','','']
            tweet_id = line[10]
            if tweet_id in g_already_finished_tweets_set:
                print('Found already in output, skipping')
                continue
            if tweet_author_id not in g_users_dict:
                try:
                    result = do_bombom(tweet_author_id)
                    majority_lang = result['user'].get('majority_lang')
                    raw_scores_eng = result['raw_scores']['english']
                    raw_scores_uni = result['raw_scores']['universal']
                    bot_score = [
                            majority_lang,
                            raw_scores_eng['astroturf'],
                            raw_scores_eng['fake_follower'],
                            raw_scores_eng['financial'],
                            raw_scores_eng['other'],
                            raw_scores_eng['overall'],
                            raw_scores_eng['self_declared'],
                            raw_scores_eng['spammer'],
                            raw_scores_uni['astroturf'],
                            raw_scores_uni['fake_follower'],
                            raw_scores_uni['financial'],
                            raw_scores_uni['other'],
                            raw_scores_uni['overall'],
                            raw_scores_uni['self_declared'],
                            raw_scores_uni['spammer']
                    ]
                    g_users_dict[tweet_author_id] = bot_score
                except:
                    bot_score = ['','','','','','','','','','','','','','','']
                    g_users_dict[tweet_author_id] = bot_score
            else:
                bot_score = g_users_dict[tweet_author_id]
            print(bot_score[0], " ", bot_score[5])
            out_line = line + bot_score
            csv_writer.writerow(out_line)
