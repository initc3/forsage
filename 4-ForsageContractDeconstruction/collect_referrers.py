#!/usr/bin/env python3

import csv
import json
import logging
from logging.handlers import RotatingFileHandler
from web3 import Web3
from web3.types import ChecksumAddress, Address
from typing import List, Dict
import forsage_abi
import time

g_logger = logging.getLogger()
g_logger.setLevel(logging.DEBUG)
g_loghandler = RotatingFileHandler('referrer_stats.log', maxBytes=int(1e7), backupCount=1)
g_loghandler.setFormatter(logging.Formatter(fmt='%(pathname)s:%(lineno)s:%(levelname)s:%(message)s'))
g_logger.addHandler(g_loghandler)

g_log_stdout = logging.getLogger('main.stdout')
#g_log_stdout.setLevel(logging.INFO)
g_log_stdout_handler = logging.StreamHandler()
g_log_stdout_handler.setLevel(logging.INFO)
g_log_stdout_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
g_log_stdout.addHandler(g_log_stdout_handler)

FORSAGE_ABI = json.loads(forsage_abi.forsage_abi)
total_addresses = 1041879
count_processed = 0
ENDPOINT = 'http://127.0.0.1:8646'
FORSAGE_CONTRACT_ADDRESS = Address(bytes.fromhex('5acc84a3e955Bdd76467d3348077d003f00fFB97'))
WEI_TO_ETH = 1000000000000000000

referrer_counts: Dict[str, int] = {}

if __name__ == "__main__":
    g_log_stdout.info('Endpoint: {}'.format(ENDPOINT))
    w3 = Web3(Web3.HTTPProvider(ENDPOINT))
    forsage = w3.eth.contract(address=FORSAGE_CONTRACT_ADDRESS, abi=FORSAGE_ABI)
    start = time.time()

    with open("../net_flow_per_addr_01_14_2021.csv", "r") as net_flow_file:
        csv_reader = csv.reader(net_flow_file)
        for line in csv_reader:
            #targ_addr = Address(bytes.fromhex("6c9acd4e7db32212797c85b1d114edc7acc5d95d"))
            targ_addr = str(line[0])
            for slot_level in range(1, 13):
                targ_x3Matrix: List = forsage.functions.usersX3Matrix(w3.toChecksumAddress(targ_addr), slot_level).call()
                targ_x6Matrix: List = forsage.functions.usersX6Matrix(w3.toChecksumAddress(targ_addr), slot_level).call()
                slot_referrer_x3: str = str(targ_x3Matrix[0]).lower()
                slot_referrer_x6: str = str(targ_x6Matrix[0]).lower()
                ref_count_x3 = referrer_counts.get(slot_referrer_x3, 0)
                referrer_counts[slot_referrer_x3] = ref_count_x3 + 1
                ref_count_x6 = referrer_counts.get(slot_referrer_x6, 0)
                referrer_counts[slot_referrer_x6] = ref_count_x6 + 1
                count_processed += 1
                if count_processed % 1000 == 0:
                    current = time.time()
                    g_log_stdout.info("Processed {} in {} seconds, {} left. Last: {}".format(count_processed, (current - start), (total_addresses - count_processed), targ_addr))
    g_log_stdout.info("Completed Lookups! Writing out CSV")
    with open("./referrer_counts_per_addr_01_14_2021.csv", "w") as out_file:
        csv_writer = csv.writer(out_file)
        for out_addr, out_count in referrer_counts.items():
            csv_writer.writerow([out_addr, out_count])

