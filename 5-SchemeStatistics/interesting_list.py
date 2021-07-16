#!/usr/bin/env python3

__author__='tyler'

import csv
import pandas as pd


# watchlist = {
#         "0xdac17f958d2ee523a2206206994597c13d831ec7": "Tether",
#         "0x8a91c9a16cd62693649d80afa85a09dbbdcb8508": "MMMBSC_Global",
#         "0x98ad263a95f1ab1abff41f4d44b07c3240251a0a": "Easy_Club",
#         "0x9e9801bace260f58407c15e6e515c45918756e0f": "WorldUnitedCoins_ERC20",
#         "0x5acc84a3e955bdd76467d3348077d003f00ffb97": "Forsage",
#         "0x8e870d67f660d95d5be530380d0ec0bd388289e1": "Paxos_Standard_Token",
#         "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": "Uniswap_V2",
#         "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": "UNI_Token",
#         "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC_Token"}


global_counter = 0


FIRST_BLOCK = 9782602
LAST_BLOCK = 10966873


def get_watchlist_txs(curr_start, curr_end, watchlist_to_handles):
    global global_counter
    merged_file_path = "{}/combined_{}.csv".format(folder_name, folder_name)
    with open(merged_file_path, 'r') as f:
        merged_data_frame = pd.read_csv(f, compression=None)
        for row in merged_data_frame.itertuples():
            if row.block_number >= FIRST_BLOCK and row.block_number <= LAST_BLOCK:
                if str(row.to_address).lower() in watchlist_to_handles:
                    handle = watchlist_to_handles[str(row.to_address).lower()]
                    handle.writerow([
                        row.hash,
                        row.block_number,
                        row.from_address,
                        row.to_address,
                        row.value,
                        row.gas_price,
                        row.gas_used,
                        row.txfee,
                        row.block_timestamp,
                        row.status,
                        ])
                    global_counter += 1
                    if global_counter % 100000 == 0:
                        print('Writing files {}'.format(global_counter))


if __name__=='__main__':
    folder_list = ["9700001_9800000", "9800001_9900000" , "9900001_10000000", "10000001_10100000", "10100001_10200000", "10200001_10300000", "10300001_10400000", "10400001_10500000", "10500001_10600000", "10600001_10700000", "10700001_10800000", "10800001_10850000", "10850001_10900000", "10900001_11000000"]


    tether_file_handle = open('Tether.csv','a')
    mmmbsc_file_handle = open('MMMBSC_Global.csv','a')
    easy_club_file_handle = open('Easy_Club.csv','a')
    worldunitedcoins_file_handle = open('WorldUnitedCoins.csv','a')
    forsage_file_handle = open('Forsage.csv','a')
    paxos_file_handle = open('Paxos.csv','a')
    uniswap_file_handle = open('Uniswap.csv','a')
    uni_file_handle = open('Unitoken.csv','a')
    usdc_file_handle = open('usdc.csv','a')

    tether_csv_writer = csv.writer(tether_file_handle)
    mmmbsc_csv_writer = csv.writer(mmmbsc_file_handle)
    easy_club_csv_writer = csv.writer(easy_club_file_handle)
    worldunitedcoins_csv_writer = csv.writer(worldunitedcoins_file_handle)
    forsage_csv_writer = csv.writer(forsage_file_handle)
    paxos_csv_writer = csv.writer(paxos_file_handle)
    uniswap_csv_writer = csv.writer(uniswap_file_handle)
    uni_csv_writer = csv.writer(uni_file_handle)
    usdc_csv_writer = csv.writer(usdc_file_handle)

    headers = ["hash","block_number","from_address","to_address","value","gas_price","gas_used","txfee","block_timestamp","status"]

    tether_csv_writer.writerow(headers)
    mmmbsc_csv_writer.writerow(headers)
    easy_club_csv_writer.writerow(headers)
    worldunitedcoins_csv_writer.writerow(headers)
    forsage_csv_writer.writerow(headers)
    paxos_csv_writer.writerow(headers)
    uniswap_csv_writer.writerow(headers)
    uni_csv_writer.writerow(headers)
    usdc_csv_writer.writerow(headers)

    watchlist_to_handles = {
        "0xdac17f958d2ee523a2206206994597c13d831ec7": tether_csv_writer,
        "0x8a91c9a16cd62693649d80afa85a09dbbdcb8508": mmmbsc_csv_writer,
        "0x98ad263a95f1ab1abff41f4d44b07c3240251a0a": easy_club_csv_writer,
        "0x9e9801bace260f58407c15e6e515c45918756e0f": worldunitedcoins_csv_writer,
        "0x5acc84a3e955bdd76467d3348077d003f00ffb97": forsage_csv_writer,
        "0x8e870d67f660d95d5be530380d0ec0bd388289e1": paxos_csv_writer,
        "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": uniswap_csv_writer,
        "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": uni_csv_writer,
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": usdc_csv_writer}

    for folder_name in folder_list:
        curr_start = int(folder_name.split("_")[0])
        curr_end = int(folder_name.split("_")[1])
        print(folder_name)
        get_watchlist_txs(curr_start, curr_end, watchlist_to_handles)

    tether_file_handle.close()
    mmmbsc_file_handle.close()
    easy_club_file_handle.close()
    worldunitedcoins_file_handle.close()
    forsage_file_handle.close()
    paxos_file_handle.close()
    uniswap_file_handle.close()
    uni_file_handle.close()
    usdc_file_handle.close()

