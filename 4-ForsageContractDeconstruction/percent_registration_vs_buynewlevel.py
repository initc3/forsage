#!/usr/bin/env python3

__author__='tyler'

import csv
import pandas as pd
from typing import Dict, List
import sys

global_counter = 0

FIRST_BLOCK = 9391396
LAST_BLOCK = 11649877

BUY_NEW_LEVEL = '0xbe389d57'
REGISTER = '0x797eee24'


count_forsage = 0
count_forsage_failed = 0
count_forsage_succeed = 0
count_buy_new_level = 0
count_register = 0
count_unrecognized = 0

unrec_list: List[str] = []

hash_to_status_dict: Dict[str, int] = {}

user_to_num_levels_bought: Dict[str, int] = {}

def write_dict_to_file():
    with open("./num_levels_bought.csv","w") as outfile:
        csv_writer = csv.writer(outfile)
        for user, num_bought in user_to_num_levels_bought.items():
            csv_writer.writerow([user, num_bought])


def get_watchlist_txs(curr_start, curr_end):
    global global_counter, count_buy_new_level, count_register, unrec_list
    global count_unrecognized, count_forsage, count_forsage_succeed, count_forsage_failed
    forsage_addr = "0x5acc84a3e955bdd76467d3348077d003f00ffb97".lower()
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    print(merged_file_path)
    print('Size of Forsage User List {}'.format(len(user_to_num_levels_bought)))
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f)
        for row in merged_data_frame.itertuples():
            if row.block_number >= FIRST_BLOCK and row.block_number <= LAST_BLOCK:
                if str(row.to_address).lower() == forsage_addr:
                    hash_to_status_dict[row.hash] = row.status
            global_counter += 1
            if global_counter % 100000 == 0:
                print('Processed {} TXs'.format(global_counter))
    transactions_file_path = "{}/transactions_{}.csv.gz".format(folder_name, folder_name)
    print(transactions_file_path)
    print('Size of Forsage User List {}'.format(len(user_to_num_levels_bought)))
    with open(transactions_file_path, 'rb') as f:
        merged_data_frame = pd.read_csv(f, compression='gzip')
        for row in merged_data_frame.itertuples():
            if row.block_number >= FIRST_BLOCK and row.block_number <= LAST_BLOCK:
                if str(row.to_address).lower() == forsage_addr:
                    count_forsage += 1
                    if hash_to_status_dict[row.hash] == 0:
                        count_forsage_failed += 1
                    elif hash_to_status_dict[row.hash] == 1:
                        count_forsage_succeed += 1
                        function_called = str(row.input)[0:10]
                        if function_called == REGISTER:
                            count_register += 1
                            if row.from_address not in user_to_num_levels_bought:
                                user_to_num_levels_bought[row.from_address] = 0
                        elif function_called == BUY_NEW_LEVEL:
                            count_buy_new_level += 1
                            # print(row.input)
                            # matrix_param = int(str(row.input)[10:74])
                            # level_param = int(str(row.input)[74:])
                            # assert level_param <= 12 and level_param >= 2, 'Matrix Level is not correct: {}'.format(level_param)
                            # assert matrix_param == 1 or matrix_param == 2, 'Matrix selected is not correct: {}'.format(matrix_param)
                            # print(matrix_param, " ", level_param)
                            tmp = user_to_num_levels_bought.get(row.from_address, 0)
                            user_to_num_levels_bought[row.from_address] = tmp+1
                        else:
                            count_unrecognized += 1
                            if row.from_address not in user_to_num_levels_bought:
                                user_to_num_levels_bought[row.from_address] = 0
                            unrec_list.append(row.hash)
                    else:
                        raise RuntimeError(row.hash)
                global_counter += 1
                if global_counter % 100000 == 0:
                    print('Processed {} TXs'.format(global_counter))


if __name__=='__main__':
    folder_list = ["9391396_9400000", "9400001_9500000", "9500001_9600000", "9600001_9700000", "9700001_9800000", "9800001_9900000" , "9900001_10000000", "10000001_10100000", "10100001_10200000", "10200001_10300000", "10300001_10400000", "10400001_10500000", "10500001_10600000", "10600001_10700000", "10700001_10800000", "10800001_10850000", "10850001_10900000", "10900001_11000000", "11000001_11100000", "11100001_11200000","11200001_11300000","11300001_11400000","11400001_11500000", "11500001_11600000", "11600001_11649877" ]


    for folder_name in folder_list:
        curr_start = int(folder_name.split("_")[0])
        curr_end = int(folder_name.split("_")[1])
        print(folder_name)
        get_watchlist_txs(curr_start, curr_end)


    print('Done')

    print('Summary Stats:')
    print('count_forsage = ', count_forsage)
    print('count_forsage_succeed = ', count_forsage_succeed)
    print('count_forsage_failed = ', count_forsage_failed)
    print('count_buy_new_level = ', count_buy_new_level)
    print('count_register = ', count_register)
    print('count_unrecognized (becomes registration) = ', count_unrecognized)
    with open('./forsage_txs_unrecognized_function_selector.csv','w') as unrec_file:
        for txhash in unrec_list:
            unrec_file.write(str(txhash) + '\n')

    write_dict_to_file()
