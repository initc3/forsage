#!/usr/bin/env python3

__author__='tyler'

import csv
import json
import pandas as pd
import statistics
import numpy as np
import sys



if __name__=='__main__':
    with open('./op_state.json','r') as f:
        state_json = json.load(f)
    op_dict_all = state_json['op_dict_all']
    op_dict_forsage = state_json['op_dict_forsage']

    op_dict_copy_sum_dupestyle_all = {}


    all_list_sstore = []
    all_list_sload = []
    all_list_call = []

    forsage_list_sstore = []
    forsage_list_sload = []
    forsage_list_call = []

    with open('txfee_all_state.csv', 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            all_list_sstore.append(row.sstore)
            all_list_sload.append(row.sload)
            all_list_call.append(row.call)
    with open('txfee_forsage_state.csv', 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            forsage_list_sstore.append(row.sstore)
            forsage_list_sload.append(row.sload)
            forsage_list_call.append(row.call)

    num_txs_all = len(all_list_sstore)
    num_txs_forsage = len(forsage_list_sstore)


    for key in op_dict_all:
        is_dupestyle = False
        for i in range(0,len(key)):#char in key:
            char = key[i]
            if char.isdigit():
                #print('{} : {}'.format(key, key[0:i]))
                aggregate_key = str(key[0:i]) + '*'
                value = op_dict_all[key]
                copy_and_sum_val = op_dict_copy_sum_dupestyle_all.get(aggregate_key, 0)
                copy_and_sum_val += value
                op_dict_copy_sum_dupestyle_all[aggregate_key] = copy_and_sum_val
                is_dupestyle = True
                break
        if not is_dupestyle:
            op_dict_copy_sum_dupestyle_all[key] = op_dict_all[key]

    op_dict_copy_sum_dupestyle_forsage = {}
    for key in op_dict_forsage:
        is_dupestyle = False
        for i in range(0,len(key)):#char in key:
            char = key[i]
            if char.isdigit():
                #print('{} : {}'.format(key, key[0:i]))
                aggregate_key = str(key[0:i]) + '*'
                value = op_dict_forsage[key]
                copy_and_sum_val = op_dict_copy_sum_dupestyle_forsage.get(aggregate_key, 0)
                copy_and_sum_val += value
                op_dict_copy_sum_dupestyle_forsage[aggregate_key] = copy_and_sum_val
                is_dupestyle = True
                break
        if not is_dupestyle:
            op_dict_copy_sum_dupestyle_forsage[key] = op_dict_forsage[key]

    op_dict_all_avgs = { key: value/num_txs_all for key,value in op_dict_copy_sum_dupestyle_all.items() }
    op_dict_forsage_avgs = { key: value/num_txs_forsage for key,value in op_dict_copy_sum_dupestyle_forsage.items() }
    # print(op_dict_all_avgs)
    # print()
    # print(op_dict_forsage_avgs)
    # print()

    print('NUM TXS ALL ', num_txs_all)
    print('NUM TXS Forsage ', num_txs_forsage)

    print('ALL CALL {}'.format(op_dict_all_avgs['CALL']))
    print('ALL CALL std {}'.format(np.std(all_list_call)))
    print('ALL CALL median {}'.format(np.median(all_list_call)))
    print('Forsage CALL {}'.format(op_dict_forsage_avgs['CALL']))
    print('Forsage CALL std {}'.format(np.std(forsage_list_call)))
    print('Forsage CALL median {}'.format(np.median(forsage_list_call)))
    print('ALL SSTORE {}'.format(op_dict_all_avgs['SSTORE']))
    print('ALL SSTORE std {}'.format(np.std(all_list_sstore)))
    print('ALL SSTORE median {}'.format(np.median(all_list_sstore)))
    print('Forsage SSTORE {}'.format(op_dict_forsage_avgs['SSTORE']))
    print('Forsage SSTORE std {}'.format(np.std(forsage_list_sstore)))
    print('Forsage SSTORE median {}'.format(np.median(forsage_list_sstore)))
    print('ALL SLOAD {}'.format(op_dict_all_avgs['SLOAD']))
    print('ALL SLOAD std {}'.format(np.std(all_list_sload)))
    print('ALL SLOAD median {}'.format(np.median(all_list_sload)))
    print('Forsage SLOAD {}'.format(op_dict_forsage_avgs['SLOAD']))
    print('Forsage SLOAD std {}'.format(np.std(forsage_list_sload)))
    print('Forsage SLOAD median {}'.format(np.median(forsage_list_sload)))

