#!/usr/bin/env python3

__author__='tyler'

import pandas as pd
import sys
import csv
from collections import Counter
import pyspark
from pyspark.sql import SparkSession

WEI_TO_ETH = 1000000000000000000
FORSAGE_ADDR = "0x5acc84a3e955Bdd76467d3348077d003f00fFB97"
GAS_FOR_SIMPLE_SEND = 21000


def wtf_txs_less_21000(curr_start, curr_end):
    folder_name = '{}_{}'.format(curr_start, curr_end)
    receipts_file_path = "{}/receipts_{}.csv.gz".format(folder_name, folder_name)
    with open(receipts_file_path, 'rb') as f2:
        receipts_data_frame = pd.read_csv(f2, compression="gzip")
        for row in receipts_data_frame.itertuples():
            if row.gas_used < 21000:
                print(row)


def do_iteration(curr_start, curr_end):
    folder_name = '{}_{}'.format(curr_start, curr_end)
    transactions_file_path = "{}/transactions_{}.csv.gz".format(folder_name, folder_name)
    receipts_file_path = "{}/receipts_{}.csv.gz".format(folder_name, folder_name)
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)

    tx_gas_used_dict = {}
    tx_status_dict = {}
    with open(receipts_file_path, 'rb') as f2:
        receipts_data_frame = pd.read_csv(f2, compression="gzip")
        counter = 0
        for row in receipts_data_frame.itertuples():
            #print(row)
            tx_gas_used_dict[row.transaction_hash] = row.gas_used
            tx_status_dict[row.transaction_hash] = row.status
            counter+=1
            if counter % 100000 == 0:
                print("Processed Receipts 100000, last TX: {}".format(row.transaction_hash))
        del receipts_data_frame

    with open(transactions_file_path, 'rb') as f:
        transactions_data_frame = pd.read_csv(f, compression="gzip")
        with open(merged_file_path, 'w') as f3:
            csv_writer = csv.writer(f3)
            headers = ['hash', 'block_number','from_address','to_address','value','gas_price','gas_used','txfee','block_timestamp','status']
            csv_writer.writerow(headers)
            counter = 0
            for row in transactions_data_frame.itertuples():
                #print(row)
                if row.hash not in tx_gas_used_dict or row.hash not in tx_status_dict:
                    raise RuntimeError(row.hash)
                curr_tx_fee = int(tx_gas_used_dict[row.hash]) * int(row.gas_price)
                curr_tx_fee = float(curr_tx_fee) / WEI_TO_ETH
                status = tx_status_dict[row.hash]
                out_line = [ row.hash,
                        row.block_number,
                        row.from_address,
                        row.to_address,
                        row.value,
                        row.gas_price,
                        tx_gas_used_dict[row.hash],
                        curr_tx_fee ,
                        row.block_timestamp,
                        status]
                csv_writer.writerow(out_line)
                counter+=1
                if counter % 100000 == 0:
                    print("Processed Transactions 100000, last TX: {}".format(row.hash))


def gather_summary_stats(curr_start, curr_end):
    top_contracts_counter = Counter()
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    stats_file_path = "{}/stats_{}.txt".format(folder_name, folder_name)
    #sc = pyspark.SparkContext('local[*]')
    #sc = pyspark.SparkContext('local')
    #spark = SparkSession.builder.appName("local").getOrCreate()
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        #merged_data_frame = spark.read.format("csv").load(f)
        #merged_data_frame.count()
        for row in merged_data_frame.itertuples():
            print("Hash {} from {} to {} with txfee {} at time {}".format(
                row.hash,
                row.from_address,
                row.to_address,
                row.txfee,
                row.block_timestamp))


def combine_all_txfees_into_one_file(global_file, curr_start, curr_end):
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            global_file.write(str(row.txfee) + '\n')

def combine_forsage_txfees_into_one_file(global_file, curr_start, curr_end):
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            if str(row.to_address).lower() == FORSAGE_ADDR.lower():
                global_file.write(str(row.txfee) + '\n')


def combine_forsage_txfees_into_one_file_no_simple(g_file_all, g_file_forsage, curr_start, curr_end):
    folder_name = '{}_{}'.format(curr_start, curr_end)
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            if row.status == 1:
                if row.gas_used != GAS_FOR_SIMPLE_SEND:
                    if str(row.to_address).lower() == FORSAGE_ADDR.lower():
                        g_file_forsage.write(str(row.txfee) + '\n')
                    g_file_all.write(str(row.txfee) + '\n')

def combine_gas_usage(g_file_all, g_file_forsage, curr_start, curr_end):
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            if row.status == 1:
                if str(row.to_address).lower() == FORSAGE_ADDR.lower():
                    g_file_forsage.write(str(row.gas_used) + '\n')
                g_file_all.write(str(row.gas_used) + '\n')

def combine_gas_usage_no_simple(g_file_all, g_file_forsage, curr_start, curr_end):
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            if row.status == 1:
                if row.gas_used != GAS_FOR_SIMPLE_SEND:
                    if str(row.to_address).lower() == FORSAGE_ADDR.lower():
                        g_file_forsage.write(str(row.gas_used) + '\n')
                    g_file_all.write(str(row.gas_used) + '\n')


if __name__ == "__main__":
    folder_list = ["9391396_9400000", "9400001_9500000", "9500001_9600000", "9600001_9700000", "9700001_9800000", "9800001_9900000" , "9900001_10000000", "10000001_10100000", "10100001_10200000", "10200001_10300000", "10300001_10400000", "10400001_10500000", "10500001_10600000", "10600001_10700000", "10700001_10800000", "10800001_10850000", "10850001_10900000", "10900001_11000000", "11000001_11100000", "11100001_11200000", "11200001_11300000", "11300001_11400000", "11400001_11500000", "11500001_11600000", "11600001_11649877"]
    #folder_list = ["9391396_9400000", "9400001_9500000"]
    #folder_list = ["9500001_9600000", "9600001_9700000", "9700001_9800000", "9800001_9900000" , "9900001_10000000", "10000001_10100000", "10100001_10200000", "10200001_10300000", "10300001_10400000", "10400001_10500000", "10500001_10600000", "10600001_10700000", "10700001_10800000", "10800001_10850000", "10850001_10900000", "10900001_11000000", "11000001_11100000", "11100001_11200000", "11200001_11300000", "11300001_11400000", "11400001_11500000", "11500001_11600000", "11600001_11649877"]
    #with open('./alltxfees.txt','w') as global_txfee_file:
    # with open('./forsagetxfees.txt','w') as global_txfee_file:
    #     for folder_name in folder_list:
    #         curr_start = int(folder_name.split("_")[0])
    #         curr_end = int(folder_name.split("_")[1])
    #         print(folder_name)
    #         #combine_all_txfees_into_one_file(global_txfee_file, curr_start, curr_end)
    #         combine_forsage_txfees_into_one_file(global_txfee_file, curr_start, curr_end)


    # for folder_name in folder_list:
    #     curr_start = int(folder_name.split("_")[0])
    #     curr_end = int(folder_name.split("_")[1])
    #     print(folder_name)
    #     # do_iteration(curr_start, curr_end)
    #     wtf_txs_less_21000(curr_start, curr_end)
    # #     #gather_summary_stats(curr_start, curr_end)

    # with open('./allsuccessgasused.txt','a') as g_all_gas_used_file:
    #     with open('./forsagesuccessgasused.txt','a') as g_forsage_gas_used_file:
    #         for folder_name in folder_list:
    #             curr_start = int(folder_name.split("_")[0])
    #             curr_end = int(folder_name.split("_")[1])
    #             print(folder_name)
    #             combine_gas_usage(g_all_gas_used_file, g_forsage_gas_used_file, curr_start, curr_end)

    # with open('./allsuccessgasused_no_simple_send.txt','a') as g_all_gas_used_file:
    #     with open('./forsagesuccessgasused_no_simple_send.txt','a') as g_forsage_gas_used_file:
    #         for folder_name in folder_list:
    #             curr_start = int(folder_name.split("_")[0])
    #             curr_end = int(folder_name.split("_")[1])
    #             print(folder_name)
    #             combine_gas_usage_no_simple(g_all_gas_used_file, g_forsage_gas_used_file, curr_start, curr_end)

    with open('./alltxfees_no_simple.txt','w') as global_txfee_file:
     with open('./forsagetxfees_no_simple.txt','w') as forsage_txfee_file:
         for folder_name in folder_list:
             curr_start = int(folder_name.split("_")[0])
             curr_end = int(folder_name.split("_")[1])
             print(folder_name)
             combine_forsage_txfees_into_one_file_no_simple(global_txfee_file, forsage_txfee_file, curr_start, curr_end)


