#!/usr/bin/env python3

__author__='tyler'

import csv
import json
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.patches as mpatches
import sys


if __name__=='__main__':
    assert len(sys.argv) == 2, str(len(sys.argv))
    if sys.argv[1] == 'txfee':
        txfee_all_array = np.ravel(np.fromfile('alltxfees_no_simple.txt', sep='\n'))
        txfee_forsage_array = np.ravel(np.fromfile('forsagetxfees_no_simple.txt', sep='\n'))
        txfee_all_edges = list(np.linspace(0, 0.06, num=100))
    elif sys.argv[1] == 'gasused':
        txfee_all_array = np.ravel(np.fromfile('allsuccessgasused_no_simple_send.txt', sep='\n'))
        txfee_forsage_array = np.ravel(np.fromfile('forsagesuccessgasused_no_simple_send.txt', sep='\n'))

        txfee_all_edges = list(np.linspace(0, 2000000, num=200))
        txfee_all_edges.append(13000000)
    else:
        print('error must specify txfee graph or gasused graph')
        sys.exit(1)

    print('all mean ',   np.mean(txfee_all_array))
    print('all stddev ', np.std(txfee_all_array))
    print('all median ',  np.median(txfee_all_array))
    print('all minval ', np.amin(txfee_all_array))
    print('all maxval ', np.amax(txfee_all_array))
    print('all 98 percentile ', np.percentile(txfee_all_array, 98, interpolation='midpoint'))
    print('all 99 percentile ', np.percentile(txfee_all_array, 99, interpolation='midpoint'))

    print('forsage mean ',   np.mean(txfee_forsage_array ))
    print('forsage stddev ', np.std(txfee_forsage_array))
    print('forsage median ',  np.median(txfee_forsage_array))
    print('forsage minval ', np.amin(txfee_forsage_array))
    print('forsage maxval ', np.amax(txfee_forsage_array))
    print('forsage 99 percentile ', np.percentile(txfee_forsage_array, 99, interpolation='midpoint'))


    print('making graphic, pray for me')
    blue =   '#3F85FF'
    orange = '#EF7700'
    fig, ax = plt.subplots()  #create figure and axes
    ax2 = ax.twinx()
    n, bins, patches = ax.hist(txfee_all_array, bins=txfee_all_edges,linewidth=0.15, edgecolor='white', label='All TXs', facecolor=blue)
    n2, bins2, patches2 = ax2.hist(txfee_forsage_array, bins=txfee_all_edges, linewidth=0.15, edgecolor='white', label='TXs to Forsage', facecolor=orange, alpha=0.7)

    ax.set_ylabel('Number of Transactions')
    ax2.tick_params(axis='y', colors=orange)
    ax.tick_params(axis='y', colors=blue)
    plt.yscale('linear')

    if sys.argv[1] == 'txfee':
        plt.xlim(0, 0.06)
        ax.set_xlabel('Transaction Cost (in Ether)')
        filename_out = "tx_fee.pdf"
        ax.set_yticks(     [ 0, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000])
        ax.set_yticklabels(['0', '5M',    '10M',    '15M',    '20M',    '25M',    '30M'])
        ax2.set_yticks(     [  0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000])
        ax2.set_yticklabels(['0', '20K', '40K', '60K', '80K', '100K', '120K', '140K','160K'])
    else:
        plt.xlim(0, 600000)
        filename_out = "tx_fee_gasused.pdf"
        ax.set_xlabel('Gas Used (in Gas)')
        ax.set_yticks(     [  0, 10000000, 20000000, 30000000, 40000000, 50000000])
        ax.set_yticklabels(['0',    '10M',    '20M',    '30M',    '40M',    '50M'])
        ax2.set_yticks(     [  0, 100000, 200000, 300000, 400000, 500000, 600000])
        ax2.set_yticklabels(['0', '100K', '200K', '300K', '400K', '500K', '600K'])


    handles = []
    handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=blue, edgecolor='black', linewidth=0.1))
    handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=orange, edgecolor='black', linewidth=0.1))
    values = ['All ETH Transactions','Forsage Transactions']
    plt.legend(handles, values, loc='upper right', fancybox=True, frameon=True, fontsize=10)

    plt.savefig(filename_out, bbox_inches="tight")
    print(filename_out)
