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
from typing import Dict, List

#address_to_num_bought: Dict[str, int] = {}
#num_bought_to_address_list: Dict[int, List[str]] = {}
# dicts seem to be slow
#num_bought_per_level: Dict[int, int] = {}

class NumBoughtPerLevelNotADict():
    level_0: List[str] = []
    level_1: List[str] = []
    level_2: List[str] = []
    level_3: List[str] = []
    level_4: List[str] = []
    level_5: List[str] = []
    level_6: List[str] = []
    level_7: List[str] = []
    level_8: List[str] = []
    level_9: List[str] = []
    level_10: List[str] = []
    level_11: List[str] = []
    level_12: List[str] = []
    level_13: List[str] = []
    level_14: List[str] = []
    level_15: List[str] = []
    level_16: List[str] = []
    level_17: List[str] = []
    level_18: List[str] = []
    level_19: List[str] = []
    level_20: List[str] = []
    level_21: List[str] = []
    level_22: List[str] = []

    def __init__(self):
        self.level_0 = []
        self.level_1 = []
        self.level_2 = []
        self.level_3 = []
        self.level_4 = []
        self.level_5 = []
        self.level_6 = []
        self.level_7 = []
        self.level_8 = []
        self.level_9 = []
        self.level_10 = []
        self.level_11 = []
        self.level_12 = []
        self.level_13 = []
        self.level_14 = []
        self.level_15 = []
        self.level_16 = []
        self.level_17 = []
        self.level_18 = []
        self.level_19 = []
        self.level_20 = []
        self.level_21 = []
        self.level_22 = []


    def insertL(self, num_bought: int, addr: str):
        if num_bought == 0:
            self.level_0.append(addr)
        elif num_bought == 1:
            self.level_1.append(addr)
        elif num_bought == 2:
            self.level_2.append(addr)
        elif num_bought == 3:
            self.level_3.append(addr)
        elif num_bought == 4:
            self.level_4.append(addr)
        elif num_bought == 5:
            self.level_5.append(addr)
        elif num_bought == 6:
            self.level_6.append(addr)
        elif num_bought == 7:
            self.level_7.append(addr)
        elif num_bought == 8:
            self.level_8.append(addr)
        elif num_bought == 9:
            self.level_9.append(addr)
        elif num_bought == 10:
            self.level_10.append(addr)
        elif num_bought == 11:
            self.level_11.append(addr)
        elif num_bought == 12:
            self.level_12.append(addr)
        elif num_bought == 13:
            self.level_13.append(addr)
        elif num_bought == 14:
            self.level_14.append(addr)
        elif num_bought == 15:
            self.level_15.append(addr)
        elif num_bought == 16:
            self.level_16.append(addr)
        elif num_bought == 17:
            self.level_17.append(addr)
        elif num_bought == 18:
            self.level_18.append(addr)
        elif num_bought == 19:
            self.level_19.append(addr)
        elif num_bought == 20:
            self.level_20.append(addr)
        elif num_bought == 21:
            self.level_21.append(addr)
        elif num_bought == 22:
            self.level_22.append(addr)
        else:
            raise RuntimeError("Should never happen")

    def get_num_per_list(self):
        return [ len(self.level_0),
                len(self.level_1),
                len(self.level_2),
                len(self.level_3),
                len(self.level_4),
                len(self.level_5),
                len(self.level_6),
                len(self.level_7),
                len(self.level_8),
                len(self.level_9),
                len(self.level_10),
                len(self.level_11),
                len(self.level_12),
                len(self.level_13),
                len(self.level_14),
                len(self.level_15),
                len(self.level_16),
                len(self.level_17),
                len(self.level_18),
                len(self.level_19),
                len(self.level_20),
                len(self.level_21),
                len(self.level_22) ]


    def getL(self, num_bought):
        if num_bought == 0:
            return self.level_0
        elif num_bought == 1:
            return self.level_1
        elif num_bought == 2:
            return self.level_2
        elif num_bought == 3:
            return self.level_3
        elif num_bought == 4:
            return self.level_4
        elif num_bought == 5:
            return self.level_5
        elif num_bought == 6:
            return self.level_6
        elif num_bought == 7:
            return self.level_7
        elif num_bought == 8:
            return self.level_8
        elif num_bought == 9:
            return self.level_9
        elif num_bought == 10:
            return self.level_10
        elif num_bought == 11:
            return self.level_11
        elif num_bought == 12:
            return self.level_12
        elif num_bought == 13:
            return self.level_13
        elif num_bought == 14:
            return self.level_14
        elif num_bought == 15:
            return self.level_15
        elif num_bought == 16:
            return self.level_16
        elif num_bought == 17:
            return self.level_17
        elif num_bought == 18:
            return self.level_18
        elif num_bought == 19:
            return self.level_19
        elif num_bought == 20:
            return self.level_20
        elif num_bought == 21:
            return self.level_21
        elif num_bought == 22:
            return self.level_22
        else:
            raise RuntimeError("Should never happen")

if __name__=='__main__':
    num_bought_to_address_list = NumBoughtPerLevelNotADict()
    with open('../data/num_levels_bought.csv', 'r') as levels_bought_file:
        csv_reader = csv.reader(levels_bought_file)
        for line in csv_reader:
            addr = str(line[0]).lower()
            num_bought = int(line[1])
            num_bought_to_address_list.insertL(num_bought, addr)
    level_y_axis_data: List[int] = num_bought_to_address_list.get_num_per_list()
    level_x_axis_data = [ i for i in range(23) ]
    print(level_x_axis_data)
    print(level_y_axis_data)
    assert len(level_x_axis_data) == len(level_y_axis_data)

    stupid_list = []
    for i in range(23):
        multiply = level_y_axis_data[i]
        appender = multiply * [ i ]
        print(appender[0:4])
        stupid_list = stupid_list + appender
    print(len(stupid_list))
    print(np.mean(stupid_list))
    print(np.std(stupid_list))
    print(np.median(stupid_list))
    sys.exit(1)

    with open('../data/net_flow_per_addr_01_14_2021.csv','r') as net_flow_file:
        reader = csv.reader(net_flow_file)
        addr_to_profits: Dict[str, float] = {str(rows[0]).lower():float(rows[1]) for rows in reader}

    profit_y_axis_data: List[float] = []
    dumb_counter = 0
    for i in level_x_axis_data:
        level_profit = 0.0
        level_list = num_bought_to_address_list.getL(i)
        for addr in level_list:
            dumb_counter += 1
            if dumb_counter % 10000 == 0:
                print('Processed addresses: ', dumb_counter)
            try:
                profit = addr_to_profits[addr]
            except KeyError:
                print('Missing address {}'.format(addr))
                continue
            level_profit += profit
        profit_y_axis_data.append(level_profit)
    print(profit_y_axis_data)
    assert len(profit_y_axis_data) == len(level_x_axis_data)



    # print('making graphic, pray for me')
    # blue =   '#3F85FF'
    # orange = '#EF7700'
    # fig, ax = plt.subplots()  #create figure and axes
    # ax2 = ax.twinx()
    # ax.bar(level_x_axis_data, height=level_y_axis_data, linewidth=0.15, edgecolor='white', label='Number of Accounts that Bought This Many Levels', facecolor=blue)
    # ax2.bar(level_x_axis_data, height=profit_y_axis_data, linewidth=0.15, edgecolor='white', label='Net Profitability of All Accounts That Bought This Many Levels', facecolor=orange, alpha=0.7)

    # ax.set_xlabel('Number of Levels Purchased')
    # ax.set_ylabel('Number of Accounts')
    # ax2.set_ylabel('Net ETH Profit/Loss')
    # ax2.tick_params(axis='y', colors=orange)
    # ax.tick_params(axis='y', colors=blue)
    # align_yaxis(ax2, 0, ax, 0)
    # #plt.yscale('linear')
    # #plt.yscale('log')
    # filename_out = "num_levels_bought_histogram.pdf"

    # # if sys.argv[1] == 'txfee':
    # #     plt.xlim(0, 0.06)
    # #     ax.set_xlabel('Transaction Cost (in Ether)')
    # #     filename_out = "tx_fee.pdf"
    # #     ax.set_yticks(     [ 0, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000])
    # #     ax.set_yticklabels(['0', '5M',    '10M',    '15M',    '20M',    '25M',    '30M'])
    # #     ax2.set_yticks(     [  0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000])
    # #     ax2.set_yticklabels(['0', '20K', '40K', '60K', '80K', '100K', '120K', '140K','160K'])


    # handles = []
    # handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=blue, edgecolor='black', linewidth=0.1))
    # handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=orange, edgecolor='black', linewidth=0.1))
    # values = ['Num Accounts That Bought This Many Levels','Net Profit of All Accounts That Bought This Many Levels']
    # plt.legend(handles, values, loc='upper right', fancybox=True, frameon=True, fontsize=10)

    # plt.savefig(filename_out, bbox_inches="tight")
    # print(filename_out)


    print('making graphic, pray for me')
    blue =   '#3F85FF'
    orange = '#EF7700'
    plt.subplot(2, 1, 1)  #create figure and axes
    pop = plt.bar(level_x_axis_data, height=level_y_axis_data, linewidth=0.15, edgecolor='white', label='Number of Accounts that Bought This Many Levels', facecolor=blue)
    plt.ylabel('Num Accounts')
    plt.yscale('log')
    plt.yticks([ 100, 1000, 10000, 100000, 1000000 ], [ "100", "1000", "10K", "100K", "1M" ])
    plt.subplot(2,1,2)
    money = plt.bar(level_x_axis_data, height=profit_y_axis_data, linewidth=0.15, edgecolor='white', label='Net Profitability of All Accounts That Bought This Many Levels', facecolor=orange, alpha=0.7)
    plt.yscale('linear')
    plt.yticks([ -30000, -20000, -10000, 0, 10000, 20000, 30000 ], [ "-30K", "-20K", "-10K", "0", "10K", "20K", "30K" ])
    plt.ylabel('Sum Profit/Loss (ETH)')

    plt.xlabel('Number of Levels Purchased')
    # ax.set_ylabel('Number of Accounts')
    # ax2.set_ylabel('Net ETH Profit/Loss')
    # ax2.tick_params(axis='y', colors=orange)
    # ax.tick_params(axis='y', colors=blue)
    #plt.yscale('linear')
    #plt.yscale('log')
    filename_out = "num_levels_bought_histogram.pdf"

    # if sys.argv[1] == 'txfee':
    #     plt.xlim(0, 0.06)
    #     ax.set_xlabel('Transaction Cost (in Ether)')
    #     filename_out = "tx_fee.pdf"
    #     ax.set_yticks(     [ 0, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000])
    #     ax.set_yticklabels(['0', '5M',    '10M',    '15M',    '20M',    '25M',    '30M'])
    #     ax2.set_yticks(     [  0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000])
    #     ax2.set_yticklabels(['0', '20K', '40K', '60K', '80K', '100K', '120K', '140K','160K'])


    plt.savefig(filename_out, bbox_inches="tight")
    print(filename_out)


