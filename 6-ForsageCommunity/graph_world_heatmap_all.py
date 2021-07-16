#!/usr/bin/env python3

__author__='tyler'

# thanks to https://matthewkudija.com/blog/2018/05/25/country-maps/
# for providing useful reference


import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import json
import sys
import math
import csv
import pycountry
import numpy as np


g_score_max = 0
g_score_min = 100000
g_twitter_country_popdata_dict = {}
g_twitter_country_count_dict = {}
g_twitter_country_count_population_adjusted_dict = {}
g_twitter_country_count_population_adjusted_highest: float = 0.00
g_twitter_score_dict = {}

g_facebook_country_popdata_dict = {}
g_facebook_country_count_dict = {}
g_facebook_country_count_population_adjusted_dict = {}
g_facebook_country_count_population_adjusted_highest: float = 0.00
g_facebook_score_dict = {}

g_youtube_country_popdata_dict = {}
g_youtube_country_count_dict = {}
g_youtube_country_count_population_adjusted_dict = {}
g_youtube_country_count_population_adjusted_highest: float = 0.00
g_youtube_score_dict = {}



#highlights = ['NGA', 'BEN', 'SYC', 'GHA', 'NAM', 'LSO', 'ZAF', 'NER', 'VEN', 'PHL', 'BGD', 'UGA']
highlights = ['SYC', 'NAM', 'LSO', 'ZAF', 'VEN', 'PHL', 'BGD', 'UGA']


europe_list = ['IRL','GBR','FRA','PRT','ESP','BEL','ITA','EST','BLR','BGR','BEL','DNK','DEU','POL','CZE','BIH','GRC','SVK','UKR','CHE','AUT','HUN','ROU','HRV','MKD','SRB','MNE','SVK','SVN', 'NOR', 'SWE', 'LVA', 'LTU', 'NLD']

africa_list = ['SEN', 'GIN', 'CIV',  'GHA',  'BEN',  'TGO',  'NGA',  'CMR',  'COG', 'NER', 'MLI']

africa2_list = ['COD','UGA','RWA','BDI','TZA','KEN','MWI','ZWE','SWZ','LSO','BWA','ZMB','MOZ']

caribbean_list = [ 'BHS', 'HTI', 'CUB', 'BLZ', 'PRI', 'DOM', 'JAM', 'GTM', 'NIC', 'SLV', 'TTO', 'CRI', 'PAN', 'COL', 'VEN' , 'SXM', 'ATG', 'VCT', 'BRB', 'CYM']

mideast_list = [ 'ISR','JOR','SYR','LBN','CYP', 'TUR', 'EGY' ]
iran_list =    [ 'IRN','SAU', 'BHR', 'QAT', 'ARE', 'KWT' ]


g_scores = {}
g_lin_color_dict = {}
g_lin_adj_color_dict = {}
g_log_color_dict = {}

FONT_SIZE = 7

g_move_label_dict3 = {
    'ZAF': (    -5,    -9,   10),
    'VEN': (     0,     1,   10),
    'NER': (   1.0,   1.5,   10),
    'NGA': (   4.0,   0.0,   10),
    'GHA': (    -5,  -5.0,   10),
    'BEN': (  -2.5,   1.0,   10),
    'LSO': (   8.0,   1.0,   10),
    'BGD': (    0,     -7,   10),
    'PHL': (   10,      0,   10),
    'UGA': (    0,      1,   10),
    'SYC': (    0,      0,   10),
    'NAM': (   -1,      0,   10),
}
g_move_label_dict2 = {
        'USA': (    9,   -6,   FONT_SIZE+1),
        'RUS': (    0,    0,   FONT_SIZE+1),
        'CAN': (   -5,   -6,   FONT_SIZE+1),
        'CHN': (    0,    0,   FONT_SIZE+1),
        'AUS': (    0,    0,   FONT_SIZE+1),
        'BRA': (    0,    0,   FONT_SIZE+1),
        'NZL': (   -4,    4,   FONT_SIZE),
        'BGD': (    0,   -6,   FONT_SIZE),
        'VNM': (  7.4, -4.4,   FONT_SIZE),
        'TWN': (    5,    0,   FONT_SIZE),
        'NPL': (    0,    1,   FONT_SIZE),
        'THA': ( -6.3,   -6,   FONT_SIZE),
        'KHM': (   -1,   -1,   FONT_SIZE),
        'MMR': (  1.7,  3.9,   FONT_SIZE),
        'LKA': (   -1,    3,   FONT_SIZE),
        'PHL': (    7,    0,   FONT_SIZE),
        'IND': ( -0.7, -1.4,   FONT_SIZE),
        'IDN': (    8,   -1,   FONT_SIZE),
        'ZAF': (    0,    0,   FONT_SIZE),
        'GEO': (    5,    5,   FONT_SIZE),
        'SOM': (    5,    0,   FONT_SIZE),
        'ECU': (    0,    1,   FONT_SIZE),
        'PER': (   -3,   -3,   FONT_SIZE),
        'PRY': (    0,  0.5,   FONT_SIZE),
        'NAM': (   -1,    3,   FONT_SIZE),
        'JPN': (    7,    0,   FONT_SIZE),
        'CHL': (   -6,    0,   FONT_SIZE),
        'URY': (    3,    0,   FONT_SIZE),
        'NCL': (    0,   -1,   FONT_SIZE),
        'DZA': (    0,   -1,   FONT_SIZE),
        'MAR': (    0,  0.2,   FONT_SIZE),
        'TUN': (    5,   -5,   FONT_SIZE),
        'UZB': (    0,    2,   FONT_SIZE),
        'YEM': (  1.5, -2.5,   FONT_SIZE),
        'ARM': (   -6, -0.3,   FONT_SIZE),
        'FIN': (    0, -0.5,   FONT_SIZE),
        'MDA': (    2,   -1,   FONT_SIZE),
        'PAK': (    2,   -2,   FONT_SIZE),
        'AFG': (    1,  1.2,   FONT_SIZE),
        'BMU': (    0,    0,   FONT_SIZE),
        'MDV': (    0, -0.3,   FONT_SIZE),
        'SDN': (   -1,    0,   FONT_SIZE),
        'ETH': (    0,   -2,   FONT_SIZE),
        'SYC': (   -3,    0,   FONT_SIZE),
        'ISL': (    1,    0,   FONT_SIZE),
        'MUS': (    0,    0,   FONT_SIZE),
        'MDG': (    0,    0,   FONT_SIZE),
        'WSM': (  -12,    2,   FONT_SIZE),
        'ARG': (    0,    0,   FONT_SIZE),
        'MYS': (  2.2,    0,   FONT_SIZE),
        'SGP': (   -1,    1,   FONT_SIZE),
        'HKG': (    0,   -3,   FONT_SIZE),
        'MNG': (    0,    0,   FONT_SIZE),
        'MAC': (   -2,  4.5,   FONT_SIZE),
        'MLT': (   -1,    3,   FONT_SIZE),
        'KOR': (    0,    0,   FONT_SIZE),
        'GRL': (    0,    0,   FONT_SIZE),
        'FJI': (    0,    3,   FONT_SIZE)
        }

for iso_code in g_move_label_dict2:
    assert iso_code not in europe_list and iso_code not in africa_list and iso_code not in africa2_list and iso_code not in caribbean_list and iso_code not in mideast_list and iso_code not in iran_list, iso_code



def choose_color(count: int) -> str:
    how_strong: float = count / g_score_max
    assert(how_strong <= 1)
    alpha: int = 10 + math.ceil(how_strong * 245) # making the scale from 10-255 rather than from 0, which is white
    alpha_str = '{:02X}'.format(alpha)
    red = '#FF0000'
    return (red + alpha_str)

def choose_color_lin(iso3: str) -> str:
    alpha: int = 10 + g_lin_color_dict[iso3]
    alpha_str = '{:02X}'.format(alpha)
    red = '#E60000'
    return (red + alpha_str)

def choose_color_lin_adj(iso3: str) -> str:
    alpha: int = 10 + g_lin_adj_color_dict[iso3]
    alpha_str = '{:02X}'.format(alpha)
    red = '#E60000'
    return (red + alpha_str)

def choose_color_log(iso3: str) -> str:
    alpha: int = 10 + g_log_color_dict[iso3]
    alpha_str = '{:02X}'.format(alpha)
    red = '#E60000'
    return (red + alpha_str)









# CALCULATIONS START

with open('../data/hootsuite-twitter-popdata/twitter-popdata.csv','r') as twitter_popdata_file:
    csv_reader = csv.reader(twitter_popdata_file)
    for line in csv_reader:
        country_code_iso3 = line[0]
        country_twitter_pop_estimate = line[1]
        #print(country_code_iso3 + ' ' + country_2019_pop_estimate)
        if country_twitter_pop_estimate != '':
            g_twitter_country_popdata_dict[country_code_iso3] = int(country_twitter_pop_estimate)

with open('../data/twitter_accounts_geo_iso.csv','r') as data_in_file:
    csv_reader = csv.reader(data_in_file)
    for line in csv_reader:
        iso_3_code = line[1]
        curr = g_twitter_country_count_dict.get(iso_3_code, 0)
        curr += 1
        g_twitter_country_count_dict[iso_3_code] = curr

for country_code_iso3, interaction_count in g_twitter_country_count_dict.items():
    pop_adjusted_interaction_count = (interaction_count / g_twitter_country_popdata_dict[country_code_iso3])
    g_twitter_country_count_population_adjusted_dict[country_code_iso3] = pop_adjusted_interaction_count
    if pop_adjusted_interaction_count > g_twitter_country_count_population_adjusted_highest:
        g_twitter_country_count_population_adjusted_highest = pop_adjusted_interaction_count

for country_code_iso3, pop_adjusted_interaction_count in g_twitter_country_count_population_adjusted_dict.items():
    g_twitter_score_dict[country_code_iso3] = (pop_adjusted_interaction_count / g_twitter_country_count_population_adjusted_highest) * 100

with open('../data/statista_id1146465_youtube-user-worldwide-2020-by-country-w-iso.csv','r') as youtube_popdata_file:
    csv_reader = csv.reader(youtube_popdata_file)
    for line in csv_reader:
        country_code_iso3 = line[1].strip()
        country_youtube_pop_estimate = line[2]
        if country_youtube_pop_estimate != '':
            g_youtube_country_popdata_dict[country_code_iso3] = int(country_youtube_pop_estimate)

with open('../data/youtube_countries.json','r') as data_in_file:
    temp_country_count_dict = json.load(data_in_file)
for key, item in temp_country_count_dict.items():
    if key != '':
        p_country = pycountry.countries.get(alpha_2=key)
        curr = g_youtube_country_count_dict.get(p_country.alpha_3, 0)
        curr = curr + item
        g_youtube_country_count_dict[p_country.alpha_3] = curr


for country_code_iso3, interaction_count in g_youtube_country_count_dict.items():
    pop_adjusted_interaction_count = (interaction_count / g_youtube_country_popdata_dict[country_code_iso3])
    g_youtube_country_count_population_adjusted_dict[country_code_iso3] = pop_adjusted_interaction_count
    if pop_adjusted_interaction_count > g_youtube_country_count_population_adjusted_highest:
        g_youtube_country_count_population_adjusted_highest = pop_adjusted_interaction_count

for country_code_iso3, pop_adjusted_interaction_count in g_youtube_country_count_population_adjusted_dict.items():
    g_youtube_score_dict[country_code_iso3] = (pop_adjusted_interaction_count / g_youtube_country_count_population_adjusted_highest) * 100



#print(g_youtube_score_dict)
#print(g_youtube_country_count_population_adjusted_dict)

with open('../data/internetworldstats-miniwatts-marketing-facebook-popdata/fb-penetration-country-03-31-2020.csv','r') as facebook_popdata_file:
    csv_reader = csv.reader(facebook_popdata_file)
    for line in csv_reader:
        country_code_iso2 = line[1].strip()
        pycountry_country = pycountry.countries.get(alpha_2=country_code_iso2)
        if pycountry_country:
            country_code_iso3 = pycountry_country.alpha_3
        else:
            if __name__ == '__main__':
                print(country_code_iso2)
            continue # this is not a bug because those countries arent in the data set actually, East Timor and Kosovo
        country_facebook_pop_estimate = line[2]
        #print(country_code_iso3 + ' ' + country_2019_pop_estimate)
        if country_facebook_pop_estimate != '':
            g_facebook_country_popdata_dict[country_code_iso3] = int(country_facebook_pop_estimate)

with open('../data/facebook-data/forsageinformationgroup-withloc-iso-byhand.csv','r') as data_in_file:
    csv_reader = csv.reader(data_in_file)
    for line in csv_reader:
        iso_3_code = line[4]
        curr = g_facebook_country_count_dict.get(iso_3_code, 0)
        curr += 1
        g_facebook_country_count_dict[iso_3_code] = curr


for country_code_iso3, interaction_count in g_facebook_country_count_dict.items():
    pop_adjusted_interaction_count = (interaction_count / g_facebook_country_popdata_dict[country_code_iso3])
    g_facebook_country_count_population_adjusted_dict[country_code_iso3] = pop_adjusted_interaction_count
    if pop_adjusted_interaction_count > g_facebook_country_count_population_adjusted_highest:
        g_facebook_country_count_population_adjusted_highest = pop_adjusted_interaction_count

for country_code_iso3, pop_adjusted_interaction_count in g_facebook_country_count_population_adjusted_dict.items():
    g_facebook_score_dict[country_code_iso3] = (pop_adjusted_interaction_count / g_facebook_country_count_population_adjusted_highest) * 100

if __name__ == '__main__':
    print("twitter")
    print(sorted(g_twitter_country_count_dict.items(), key=lambda item: item[1]))
    print("facebook")
    print(sorted(g_facebook_country_count_dict.items(), key=lambda item: item[1]))
    print("youtube")
    print(sorted(g_youtube_country_count_dict.items(), key=lambda item: item[1]))
    #print(g_facebook_score_dict)

all_gross_social_dict = {}
sum_twitter = 0
sum_facebook = 0
sum_youtube = 0
for key, value in g_twitter_country_count_dict.items():
    all_gross_social_dict[key] =  value
    sum_twitter += value
for key, value in g_facebook_country_count_dict.items():
    curr = all_gross_social_dict.get(key, 0)
    curr += value
    all_gross_social_dict[key] =  curr
    sum_facebook += value
for key, value in g_youtube_country_count_dict.items():
    curr = all_gross_social_dict.get(key, 0)
    curr += value
    all_gross_social_dict[key] =  curr
    sum_youtube += value

if __name__ == '__main__':
    print("gross")
    print(sorted(all_gross_social_dict.items(), key=lambda item: item[1]))


# Print out top countries to a separate CSV for table in the paper
# make_me_a_csv = ['NGA', 'PHL', 'IND', 'USA', 'IDN', 'ZAF', 'PAK', 'MYS', 'AUS', 'GBR', 'RUS']
# header = ['Country', 'Facebook', 'Twitter', 'YouTube']
# with open('gross_social_media.csv', 'w') as gross_social_media_file:
#     csv_writer = csv.writer(gross_social_media_file)
#     csv_writer.writerow(header)
#     for element in make_me_a_csv:
#         csv_writer.writerow([element,
#             g_facebook_country_count_dict.get(element, 0),
#             g_twitter_country_count_dict.get(element, 0)])
#             #g_youtube_country_count_dict.get(element, 0)])
#     csv_writer.writerow(['TOTAL', sum_facebook, sum_twitter, sum_youtube ])


# for iso3, score in g_twitter_score_dict.items():
#     curr = g_scores.get(iso3, 0)
#     curr += score
#     g_scores[iso3] = curr
# for iso3, score in g_facebook_score_dict.items():
#     curr = g_scores.get(iso3, 0)
#     curr += score
#     g_scores[iso3] = curr
# for iso3, score in g_youtube_score_dict.items():
#     curr = g_scores.get(iso3, 0)
#     curr += score
#     g_scores[iso3] = curr
# g_score_max = 300
# print(g_scores)

for iso3, pop in g_twitter_country_count_population_adjusted_dict.items():
    curr = g_scores.get(iso3, 0)
    curr += pop
    g_scores[iso3] = curr
for iso3, pop in g_facebook_country_count_population_adjusted_dict.items():
    curr = g_scores.get(iso3, 0)
    curr += pop
    g_scores[iso3] = curr
# for iso3, pop in g_youtube_country_count_population_adjusted_dict.items():
#     curr = g_scores.get(iso3, 0)
#     curr += pop
#     g_scores[iso3] = curr
for iso3, score in g_scores.items():
    # removing youtube since dataset is small af
    #div3_times_100k = (score / 3) * 100000
    div2_times_100k = (score / 2) * 100000
    #g_scores[iso3] = div3_times_100k
    g_scores[iso3] = div2_times_100k
g_scores_list = []
for iso3, score in g_scores.items():
    g_scores_list.append(score)
    if score > g_score_max:
        # removing outliers for map coloring
        if iso3 != 'NGA' and iso3 != 'BEN':
            g_score_max = score
        #g_score_max = score
    if score < g_score_min:
        g_score_min = score

g_score_arr = np.asarray(g_scores_list)

lin_space = np.linspace(g_score_min, g_score_max, num=245)
log_space = np.geomspace(g_score_min, g_score_max, num=245) # 10-255 for alpha for colors

lin_space_adj = np.linspace(g_score_min, np.percentile(g_score_arr, 90, interpolation='nearest'), num=245)

lin_space[0] = 0
lin_space[-1] = lin_space[-1] + 1000
log_space[0] = 0
log_space[-1] = log_space[-1] + 1000

lin_space_adj[0] = 0
outliers = np.linspace(np.percentile(g_score_arr, 90, interpolation='nearest') + 0.1, 125, num=9)
for i in range(-9, 0):
    lin_space_adj[i] = outliers[i]

# manually do binning I guess
# yes this is slow as *** O(n) for each score but who cares
for iso3, score in g_scores.items():
    for i in range(len(log_space)):
        if score > log_space[i] and score < log_space[i+1]:
            g_log_color_dict[iso3] = i
            break
    for i in range(len(lin_space)):
        if score > lin_space[i] and score < lin_space[i+1]:
            g_lin_color_dict[iso3] = i
            break
    for i in range(len(lin_space_adj)):
        if score > lin_space_adj[i] and score < lin_space_adj[i+1]:
            g_lin_adj_color_dict[iso3] = i
            break

assert len(g_log_color_dict) == len(g_scores), '{} != {}'.format(len(g_log_color_dict), len(g_scores))
assert len(g_lin_color_dict) == len(g_scores), '{} != {}'.format(len(g_lin_color_dict), len(g_scores))
assert len(g_lin_adj_color_dict) == len(g_scores), '{} != {}'.format(len(g_lin_adj_color_dict), len(g_scores))

# lin_sort = dict(sorted(g_lin_color_dict.items(), key=lambda item: item[1]))
# adj_sort = dict(sorted(g_lin_adj_color_dict.items(), key=lambda item: item[1]))
# for key, value in lin_sort.items():
#     if value != adj_sort[key]:
#         print('{} | {} | {}'.format(key, value, adj_sort[key]))

if __name__ == '__main__':
    # Defaults to 5.36 × 2.92  inches
    fig_width_inches = 5.36 * 2
    fig_height_inches = 2.92 * 2
    fig = plt.figure(figsize=(fig_width_inches, fig_height_inches))

    projection = ccrs.Robinson()
    #title = 'Forsage Social Media Interaction Heatmap by Country (Per 100k People)'

    ax = plt.axes(projection=projection)
    ax.add_feature(cartopy.feature.OCEAN, facecolor='white')
    ax.spines['geo'].set_edgecolor('black')
    ax.spines['geo'].set_linewidth(0.1)

    # uncomment before running the blown up maps
    # with open('../data/social-media-country-per100k-scores.csv', 'w') as smcp100ksfile:
    #     # countries_with_shapes = []
    #     csv_writer_SMCP100ksfile = csv.writer(smcp100ksfile)
    #     shpfilename2 = shpreader.natural_earth(resolution='10m',
    #                                           category='cultural',
    #                                           name='admin_0_countries')
    #     reader2 = shpreader.Reader(shpfilename2)
    #     countries2 = reader2.records()
    #     for country2 in countries2:
    #         iso_code = country2.attributes['ADM0_A3']
    #         print(iso_code)
    #         csv_writer_SMCP100ksfile.writerow([iso_code, g_scores.get(iso_code, 0)])
    #     #     countries_with_shapes.append(country.attributes['ADM0_A3'])
    #     # for iso_code in g_scores:
    #     #     assert iso_code in countries_with_shapes, iso_code
    # sys.exit(1)



    shpfilename = shpreader.natural_earth(resolution='50m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    for country in countries:
        iso_code = country.attributes['ADM0_A3']
        f_color = '#ABABAB'
        if iso_code in g_scores:
            #f_color = choose_color(g_scores[iso_code])
            #f_color = choose_color_log(iso_code)
            f_color = choose_color_lin_adj(iso_code)


        ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                          facecolor=f_color,
                          label=iso_code,
                          edgecolor='#999999',
                          linewidth=.1)
        if iso_code in g_scores:
            x = country.geometry.centroid.x
            y = country.geometry.centroid.y
            size = FONT_SIZE
            if iso_code in g_move_label_dict3:
                x2, y2, s2 = g_move_label_dict3[iso_code]
                x = x + x2
                y = y + y2
                size = s2
            score = g_scores[iso_code]
            if score >= 0.01:
                score = "{:.2f}".format(score)
            elif score >= 0.001:
                score = "{:.3f}".format(score)
            else:
                score = "{:.4f}".format(score)
            #if iso_code not in europe_list and iso_code not in africa_list and iso_code not in africa2_list and iso_code not in caribbean_list and iso_code not in mideast_list and iso_code not in iran_list:
            if iso_code in highlights:
                score = iso_code + '\n' + score
                ax.text(x, y, score, color='black', size=size, ha='center', va='center', transform=ccrs.PlateCarree())

    # legend
    handles = []
    handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor='#ABABAB', edgecolor='black', linewidth=0.1))
    handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor='red', edgecolor='black', linewidth=0.1))
    values = ['No interaction/No Data','Interaction']
    plt.legend(handles, values,
               loc='lower left', bbox_to_anchor=(0.025, -0.0),
               fancybox=True, frameon=True, fontsize=5)
               #edgecolor='black', facecolor='white')#, linewidth=0.1, )


    #plt.title(title, fontsize=8)

    title = '../results/countries-heatmap-all-partlabels.pdf'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))

    print('Done.\n')


