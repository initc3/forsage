#!/usr/bin/env python3

__author__ = 'tyler'

import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import ScalarFormatter
import math
from typing import List
import sys
import numpy as np

# the below section of code graphs a histogram of the data in the net_flow CSV
really_small_losers_and_winner = []
net_list = []
net_min = 0.0
net_max = 0.0

with open('../data/net_flow_per_addr_01_14_2021.csv','r') as n_f:
    csv_reader = csv.reader(n_f)
    for line in csv_reader:
        val = float(line[1])
        #net_dict[line[0]] = val
        net_list.append(val)
        if val < net_min:
            net_min = val
        if val > net_max:
            net_max = val
        if val <= 1.25 and val >= -1.25:
            really_small_losers_and_winner.append(val)

print(net_min)
print(net_max)
my_edges = []
# for i in np.linspace(net_min-1, -0.00001, num=100):
#     my_edges.append(i)
# my_edges.append(0)
# for i in np.linspace(0.00001, net_max+1, num=100):
#     my_edges.append(i)
for i in np.linspace(net_min-1, net_max+1, num=200):
    my_edges.append(i)
last = -10000000000
new_my_edges = []
count_negative = 0
for i in my_edges:
    assert(i > last)
    if i < 0:
        count_negative += 1
    if i > 0 and last < 0:
        count_negative += 1
        new_my_edges.append(0)
    new_my_edges.append(i)
    last = i
my_edges = new_my_edges

hist, bin_edges = np.histogram(a=net_list, bins=my_edges)

# my_edges = []
# for i in np.linspace(net_min-10, -0.1, num=20):
#     my_edges.append(i)
# my_edges.append(0)
# for i in np.linspace(0.1, net_max+10, num=20):
#     my_edges.append(i)
# hist, bin_edges = np.histogram(a=net_list, bins=my_edges)


print(hist)
print_bin_edges = []
for ele in bin_edges:
    print_bin_edges.append('{:f}'.format(ele).rstrip('0'))
print(print_bin_edges)
print(count_negative)

plt.rcParams.update({'font.size': 22})
#plt.rcParams.update({'xtick.labelsize': 'xx-small'})    # fontsize of the tick labels

fig, ax = plt.subplots(figsize=(12,12))
ax_N, ax_bins, ax_patches = ax.hist(net_list, bins=my_edges, linewidth=0.15, edgecolor='white', facecolor='forestgreen')
for i in range(0, count_negative):
    ax_patches[i].set_facecolor('r')

curr_xlim = plt.xlim()
#print(curr_xlim)
manually_setting_xticks = list(np.arange(0, 5500, 500))
manually_setting_xticks = [-250, 0, 250] + manually_setting_xticks


plt.xlim(-250, 5500)
#plt.xticks(manually_setting_xticks)
#plt.rcParams.update({'xtick.labelsize': 'medium'})    # fontsize of the tick labels fontsize=7,
plt.xticks(manually_setting_xticks,  rotation=45, rotation_mode = 'anchor', ha = 'right')
plt.xlabel('Net Gain/Loss (ETH)')
plt.yscale('log')
for axis in [ax.xaxis, ax.yaxis]:
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    axis.set_major_formatter(formatter)
plt.ylabel('Number of Users')
plt.yticks([1, 10, 100, 1000, 10000, 100000, 1000000], ["1", "10", "100", "1K", "10K", "100K", "1M"])
#plt.title('Forsage Profit & Loss Distribution')
red_patch = mpatches.Patch(color='red', label='User with Net Loss')
green_patch = mpatches.Patch(color='forestgreen', label='User with Net Profit')
plt.legend(handles=[red_patch, green_patch])
figtitle = "../results/profit_histogram_all_01_14_2021.pdf"
fig.savefig(figtitle, bbox_inches="tight")
print(figtitle)

sys.exit(0)

really_small_edges: List[float] = []
for i in np.linspace(-1.25, 1.25, num=100):
    really_small_edges.append(i)
last = -3
new_really_small_edges = []
count_negative = 0
for i in really_small_edges:
    assert(i > last)
    if i < 0:
        count_negative += 1
    if i > 0 and last < 0:
        count_negative += 1
        new_really_small_edges.append(0.0)
    new_really_small_edges.append(i)
    last = i
really_small_edges = new_really_small_edges
hist, bin_edges = np.histogram(a=really_small_losers_and_winner, bins=really_small_edges)


plt.rcParams.update({'xtick.labelsize': 'medium'})    # fontsize of the tick labels
print(hist)
print(bin_edges)
print(really_small_edges)
fig, ax = plt.subplots(figsize=(15,8))
ax_N, ax_bins, ax_patches = ax.hist(really_small_losers_and_winner, bins=really_small_edges, linewidth=0.15, edgecolor='white', facecolor='forestgreen')
for i in range(0, count_negative):
    ax_patches[i].set_facecolor('r')

plt.xlabel('Net Gain/Loss (ETH)')
plt.xticks(np.arange(-1.25, 1.5, 0.25))
#plt.yscale('log')
for axis in [ax.xaxis, ax.yaxis]:
    axis.set_major_formatter(ScalarFormatter())
ax.set_ybound(100, 225000)
plt.ylabel('Number of Users')
#plt.title('Forsage Profit & Loss Distribution, Really Small Values')
plt.yticks([25000, 50000, 75000 , 100000, 125000, 150000, 175000, 200000, 225000], ["25K", "50K", "75K", "100K", "125K", "150K", "175K", "200K", "225K"])
red_patch = mpatches.Patch(color='red', label='User with Net Loss')
green_patch = mpatches.Patch(color='forestgreen', label='User with Net Profit')
plt.legend(handles=[red_patch, green_patch])
figtitle="../results/profit_histogram_cluster_01_14_2021-2.pdf"
fig.savefig(figtitle, bbox_inches="tight")
print(figtitle)


