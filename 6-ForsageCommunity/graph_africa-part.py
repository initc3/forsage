#!/usr/bin/env python3

__author__='tyler'

import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import json
import sys
import math
import pprint
import csv
import pycountry
import numpy as np
import graph_world_heatmap_all


g_scores = {}
g_count_max = 0
g_score_min = 100000

g_move_label_dict2 = {
#        'SEN': (-0.7,0.8,13),
#       'GIN': (0,0.2,13),
#       'CIV': (0,-0.5,13),
        'GHA': (-0.2,1.5,15),
        'BEN': (0,1.13,15),
        'TGO': (0,-1.2,15),
        'NGA': (0,0,22),
#       'CMR': (0,-0.5,13),
#       'COG': (0.2,0.2,13),
        'NER': (0,-2,18),
#       'MLI': (0, -1.8, 13)
        }


def choose_color(count: int) -> str:
    how_strong: float = count / g_count_max
    assert(how_strong <= 1)
    alpha: int = 10 + math.ceil(how_strong * 245) # making the scale from 10-255 rather than from 0, which is white
    alpha_str = '{:02X}'.format(alpha)
    red = '#FF0000'
    return (red + alpha_str)


if __name__ == '__main__':
    with open('../data/social-media-country-per100k-scores.csv', 'r') as smcp100ksfile:
        csv_reader = csv.reader(smcp100ksfile)
        for line in csv_reader:
            score = float(line[1])
            g_scores[str(line[0])] = score
            if score > g_count_max:
                g_count_max = score
            if score < g_score_min:
                g_score_min = score

    projection = ccrs.LambertAzimuthalEqualArea()
    ax = plt.axes(projection=projection)

    #extent = [-17.2, 17.2, -4.9, 17 ]
    extent = [-4, 15.2,  1.0, 17 ]
    ax.set_extent(extent)

    ax.add_feature(cartopy.feature.OCEAN, facecolor='white')
    ax.spines['geo'].set_edgecolor('black')
    ax.spines['geo'].set_linewidth(0.1)

    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    #with open('../data/social-media-country-per100k-scores.csv', 'w') as smcp100ksfile:
    #    csv_writer = csv.writer(smcp100ksfile)

    for country in countries:
        iso_code = country.attributes['ADM0_A3']
        f_color = '#ABABAB'
        if g_scores[iso_code] > 0:
            #f_color = choose_color(g_scores[iso_code])
            f_color = graph_world_heatmap_all.choose_color_lin_adj(iso_code)


        ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                          facecolor=f_color,
                          label=iso_code,
                          edgecolor='#000000',
                          linewidth=.1)

        x = country.geometry.centroid.x
        y = country.geometry.centroid.y
        size = 5
        if iso_code in g_move_label_dict2:
            x2, y2, s2 = g_move_label_dict2[iso_code]
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
        if iso_code in g_move_label_dict2 and g_scores[iso_code] > 0:
            score = iso_code + '\n' + score
            ax.text(x, y, score, color='black', size=size, ha='center', va='center', transform=ccrs.PlateCarree())



    title = '../results/countries-heatmap-africa-part.pdf'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))

    print('Done.\n')


