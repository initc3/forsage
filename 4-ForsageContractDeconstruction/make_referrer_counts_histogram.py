#!/usr/bin/env python3

from typing import List, Dict
import csv
import sys
import numpy as np

import matplotlib.pyplot as plt

referrer_counts_per_addr_01_14_2021_csv_len =  611795
net_flow_per_addr_01_14_2021_csv_len        = 1041879

num_referrer_for_nobody = net_flow_per_addr_01_14_2021_csv_len - referrer_counts_per_addr_01_14_2021_csv_len
#print(num_referrer_for_nobody)

list_referrer_counts: List[int] = [0]*num_referrer_for_nobody
dict_referrer_counts: Dict[int, List[str]] = {}
dict_addr_to_count: Dict[str, int] = {}
counts_to_profits: Dict[int, float] = {}

with open("../data/referrer_counts_per_addr_01_14_2021.csv","r") as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        addr = str(line[0])
        count = int(line[1])
        if addr == "0x0000000000000000000000000000000000000000":
            continue
        list_referrer_counts.append(count)
        #dict_referrer_counts[count] = dict_referrer_counts.get(count, []) + [addr]
        dict_addr_to_count[addr] = count

with open("../data/net_flow_per_addr_01_14_2021.csv","r") as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        addr = str(line[0])
        profit = float(line[1])
        if addr not in dict_addr_to_count:
            dict_addr_to_count[addr] = 0
            #dict_referrer_counts[0] = dict_referrer_counts.get(0, []) + [ addr ]
        count = dict_addr_to_count[addr]
        counts_to_profits[count] = counts_to_profits.get(count, 0) + profit



count_hist, bin_edges = np.histogram(list_referrer_counts, bins=210)
profit_hist = [0.0]*211
#print(len(bin_edges))
#print(len(profit_hist))

for q in range(0, int(bin_edges[-1]+1)):
    for i in range(0, 211):
        edge = bin_edges[i]
        if i == 210:
            edge_2 = 10000000000000000
        else:
            edge_2 = bin_edges[i+1]
        if q >= edge and q < edge_2:
            profit_hist[i] = profit_hist[i] + counts_to_profits.get(q, 0.0)


#print(profit_hist)

print(count_hist[-1])
print(bin_edges[-1])
print(bin_edges[-2])

#print(count_hist[0:10])
#print(bin_edges[0:10])
#print(bin_edges[-1])

#print(np.mean(list_referrer_counts))
#print(np.std(list_referrer_counts))
#print(np.median(list_referrer_counts))
#print(num_referrer_for_nobody)

# n, bins, patches = plt.hist(list_referrer_counts, bins=210,linewidth=0.15, edgecolor='white', label='All TXs', facecolor='tab:blue')
# plt.xlabel('Num Slot Referrals Set')
# plt.ylabel('Num Users')
# plt.yscale('log')
# plt.yticks([1, 10, 100, 1000, 10000, 100000, 1000000], ["1", "10", "100", "1K", "10K", "100K", "1M"])
# plt.xticks([0, 1000, 2000, 4000, 6000, 8000, 10000], ["0", "1K", "2K", "4K", "6K", "8K", "10K"])
# figname = "../results/referrer_count_histogram.pdf"
# plt.savefig(figname, bbox_inches="tight")
# print(figname)


print('making graphic, pray for me')
blue =   '#3F85FF'
orange = '#EF7700'
plt.subplot(2, 1, 1)  #create figure and axes
print(len(bin_edges), " " , len(profit_hist))
print(len(bin_edges), " " , len(count_hist))
plt.bar(bin_edges[0:len(bin_edges)-1], height=count_hist, linewidth=0.15, edgecolor='white', label='Number of Accounts that Bought This Many Levels', facecolor=blue)
plt.xlabel('Num Slot Referrals Set')
plt.ylabel('Num Users')
plt.yscale('log')
#plt.yticks([1, 10, 100, 1000, 10000, 100000, 1000000], ["1", "10", "100", "1K", "10K", "100K", "1M"])
#plt.xticks([0, 1000, 2000, 4000, 6000, 8000, 10000], ["0", "1K", "2K", "4K", "6K", "8K", "10K"])
plt.subplot(2,1,2)
money = plt.bar(bin_edges, height=profit_hist, linewidth=0.15, edgecolor='white', label='Net Profitability of All Accounts That Bought This Many Levels', facecolor=orange, alpha=0.7)
plt.yscale('linear')
plt.ylabel('Sum Profit/Loss (ETH)')
figname = "../results/referrer_count_histogram_w_profit.pdf"
plt.savefig(figname, bbox_inches="tight")
print(figname)

