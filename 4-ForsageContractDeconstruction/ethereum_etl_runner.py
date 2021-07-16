#!/usr/bin/env python3

import os
import subprocess
import sys

#START_BLOCK=11000001
#END_BLOCK=11649877
manual_list = [(9241022, 9300000), (9300001, 9391530)]

#for curr_start in range(START_BLOCK, END_BLOCK, 100000):
for curr_start, curr_end in manual_list:
    #curr_end = curr_start+99999 # changed from 9
    #if curr_end > END_BLOCK:
    #    curr_end = END_BLOCK
    folder_name = '{}_{}'.format(curr_start, curr_end)
    os.mkdir(folder_name)
    cmd = [
            "ethereumetl",
            "export_blocks_and_transactions",
            "--start-block",
            str(curr_start),
            "--end-block",
            str(curr_end),
            "--blocks-output",
            "{}/blocks_{}.csv".format(folder_name,folder_name),
            "--transactions-output",
            "{}/transactions_{}.csv".format(folder_name,folder_name),
            "--provider-uri",
            "http://127.0.01:8646"
    ]


    process = subprocess.Popen(cmd, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process.stdout:
        for line in iter(process.stdout.readline, ''):
            print(line,end='')
            sys.stdout.flush()
        process.wait()

    cmd2 = [
            "ethereumetl",
            "extract_csv_column",
            "--input",
            "{}/transactions_{}.csv".format(folder_name, folder_name),
            "--column",
            "hash",
            "--output",
            "{}/transaction_hashes_{}.txt".format(folder_name,folder_name)
    ]


    process2 = subprocess.Popen(cmd2, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process2.stdout:
        for line in iter(process2.stdout.readline, ''):
            print(line,end='')
            sys.stdout.flush()
        process2.wait()


    cmd3 = [
            "ethereumetl",
            "export_receipts_and_logs",
            "--transaction-hashes",
            "{}/transaction_hashes_{}.txt".format(folder_name, folder_name),
            "--provider-uri",
            "http://127.0.01:8646",
            "--receipts-output",
            "{}/receipts_{}.csv".format(folder_name,folder_name)
    ]
    process3 = subprocess.Popen(cmd3, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process3.stdout:
        for line in iter(process3.stdout.readline, ''):
            print(line,end='')
            sys.stdout.flush()
        process.wait()


