#!/usr/bin/env python3

__author__ = 'tyler'
import csv
import math
import sys

failed_tx_dict = dict()
gas_dict = dict()
send_to_dict = dict()
recv_from_dict = dict()
all_addresses_seen = set()

# proxy contracts, Alice -> contract -> Forsage
special_addresses_failed = dict()
special_addresses_seen_to = set()
special_addresses_seen_from = set()

#net_dict = dict()
#net_list = list()
net_min = 0
net_max = 0

WEI_TO_ETH = 1000000000000000000

# this sums up statistics from the
# existing traces and txs files we have and creates the net
# profit and loss CSV

with open('../data/to_forsage_txs_01_14_2021.csv','r') as t_g:
    csv_reader = csv.reader(t_g)
    next(csv_reader)
    for line in csv_reader:
        tx_hash = str(line[0]).lower()
        reciept_status = bool(int(line[7]))
        failed_tx_dict[tx_hash] = reciept_status
        from_addr = str(line[1]).lower()
        all_addresses_seen.add(from_addr)
        gas_price = int(line[5])
        gas_used = int(line[6])
        val = gas_price * gas_used
        current_sum = gas_dict.get(from_addr, 0)
        gas_dict[from_addr] = current_sum + val

with open('../data/bad_txs_forsage_01_14_2021.csv','r') as t_b:
    csv_reader = csv.reader(t_b)
    next(csv_reader)
    #hash,from_address,to_address,value,gas,gas_price,receipt_gas_used,receipt_status,block_number,transaction_index,block_timestamp
    for line in csv_reader:
        tx_hash = str(line[0]).lower()
        reciept_status = bool(int(line[7]))
        special_addresses_failed[tx_hash] = reciept_status
        from_addr = str(line[1]).lower()
        to_addr = str(line[2]).lower()
        if to_addr == '':
            # corner case, transaction that spawned the Forsage contract itself
            continue
        special_addresses_seen_from.add(from_addr)
        special_addresses_seen_to.add(to_addr)
        gas_price = int(line[5])
        gas_used = int(line[6])
        val = gas_price * gas_used
        current_sum = gas_dict.get(from_addr, 0)
        gas_dict[from_addr] = current_sum + val

err_from = 0
with open('../data/from_forsage_traces_01_14_2021.csv','r') as t_f:
    csv_reader = csv.reader(t_f)
    next(csv_reader)
    for line in csv_reader:
        tx_hash = str(line[0]).lower()
        if tx_hash not in failed_tx_dict:
            if tx_hash not in special_addresses_failed:
                print('Error tx hash not in all from txs ', tx_hash)
                err_from += 1
                continue
            reciept_status = special_addresses_failed[tx_hash]
        else:
            reciept_status = failed_tx_dict[tx_hash]
        to_addr = str(line[2]).lower()
        all_addresses_seen.add(to_addr)
        if reciept_status:
            val = int(line[3])
            current_sum = recv_from_dict.get(to_addr, 0)
            recv_from_dict[to_addr] = current_sum + val

err_to = 0
with open('../data/to_forsage_traces_01_14_2021.csv','r') as t_t:
    csv_reader = csv.reader(t_t)
    next(csv_reader)
    for line in csv_reader:
        tx_hash = str(line[0]).lower()
        if tx_hash not in failed_tx_dict:
            if tx_hash not in special_addresses_failed:
                print('Error tx hash not in all to txs ', tx_hash)
                err_to += 1
                continue
            else:
                reciept_status = special_addresses_failed[tx_hash]
        else:
            reciept_status = failed_tx_dict[tx_hash]
        from_addr = str(line[1]).lower()
        all_addresses_seen.add(from_addr)
        if reciept_status:
            val = int(line[3])
            current_sum = send_to_dict.get(from_addr, 0)
            send_to_dict[from_addr] = current_sum + val

# owner corner case
owner = '0x81ca1e4de24136ebcf34ca518af87f18fd39d45e'.lower()
#owner_recv = (recv_from_dict.get(owner, 0.0)) / WEI_TO_ETH
#owner_send = (send_to_dict.get(owner, 0.0)) / WEI_TO_ETH
owner_gas = 13403200000000000 # 0.0134032 # from etherscan https://etherscan.io/tx/0x65189e6e311cf0366a78b809ff04f3f66d712973fa8416ee5a3a67c7d8027667
if not (owner in gas_dict):
    gas_dict[owner] = owner_gas
else:
    print('Owner was already in gas dict', gas_dict[owner])
    curr_gas = gas_dict[owner]
    gas_dict[owner] = owner_gas + curr_gas
all_addresses_seen.add(owner)

num_not_in_dict = 0
num_err_no_tx = 0
with open('../data/net_flow_per_addr_01_14_2021.csv','w') as n_f:
    csv_writer = csv.writer(n_f)
    for addr in all_addresses_seen:#, gas_value in gas_dict.items():
        if not (addr in send_to_dict):
            # since the tx collection happened a bit later after the
            # traces collection there are some new addresses in the
            # txs we dont have trace data for
            if not (addr in recv_from_dict):
                num_not_in_dict += 1
                continue
            # cases where someone used a contract that then called
            # the forsage contract. The accounting here might be off...
            elif not (addr in gas_dict):
                num_err_no_tx += 1
                send_value = 0.0
            else:
                if addr != owner:
                    raise KeyError("Should never happen {}".format(addr))
                else:
                    send_value = 0.0
        else:
            send_value = float(send_to_dict[addr]) / WEI_TO_ETH
        recv_value = float(recv_from_dict.get(addr, 0)) / WEI_TO_ETH
        gas_value = float(gas_dict.get(addr, 0)) / WEI_TO_ETH
        out_value = send_value + gas_value
        net_value = recv_value - out_value
        #net_dict[addr] = net_value
        #print(net_value)
        #net_list.append(net_value)
        if net_value < net_min:
            net_min = net_value
        if net_value > net_max:
            net_max = net_value
        csv_writer.writerow([addr, net_value])

print('err from', err_from)
print('err to', err_to)
print('Number from future ', num_not_in_dict)
print('Number using contract proxies ', num_err_no_tx)
print('Net min ', net_min)
print('Net max ', net_max)

print('failed_tx_dict dict ', len(failed_tx_dict))
print('gas_dict dict ', len(gas_dict))
print('send_to_dict dict ', len(send_to_dict))
print('recv_from_dict dict ', len(recv_from_dict))
print('all_addresses_seen set ', len(all_addresses_seen))

# doing this to confirm data matches prior expectations
with open('../data/net_flow_per_addr_nogas_01_14_2021.csv','w') as n_f:
    csv_writer = csv.writer(n_f)
    for addr in all_addresses_seen:
        sent_value = (send_to_dict.get(addr, 0.0)) / WEI_TO_ETH
        recv_value = (recv_from_dict.get(addr, 0.0)) / WEI_TO_ETH
        if send_value == 0.0 and recv_value > 0:
            print(addr)
        net_nogas = recv_value - sent_value
        # print(net_nogas)
        csv_writer.writerow([addr, net_nogas])
