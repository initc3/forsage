#!/usr/bin/env python3

__author__='tyler'

from web3 import Web3
from web3.geth import GethMiner
from web3.types import TxReceipt#, Contract
import csv
from typing import Dict, List, TypedDict, Optional, Tuple, Any, Set
import json
import logging
import pprint
from expiriment_constants import Address, X3, X6, User, ONE_GWEI, GAS_MAX, wei_to_eth, eth_to_Wei, MutableBool, MutableInt, MutableString
from eth_typing import ChecksumAddress, HexStr, HexAddress
from graphing import graph_full_state, graph_full_state_per_user
import sys
import random
import warnings
from enum import Enum

g_human_names = ['miner', 'alpha', 'bravo', 'charlie', 'delta', 'echo',
        'foxtrot', 'golf', 'hotel', 'india', 'juliet', 'kilo',
        'lima', 'mike', 'november', 'oscar', 'papa', 'quebec',
        'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'xray', 'zulu']
g_address_list: List[str] = [] # List of public keys
g_address_dict: Dict[str, Address] = {} # indexed by public eth address
g_active_user_dict: Dict[str, User] = {} # indexed by human name
g_names_pubkey_dict: Dict[str, str] = {} # indexed by name to public key

g_forsage_contract = None


g_address_dict['0x0000000000000000000000000000000000000000'] = Address({ 'human_name': '0x0', 'private_key': 'whoknows', 'addr': '0x0000000000000000000000000000000000000000', 'balance': 0, 'balance_start': 0}) # saves headache on some corner case checking

def pick_random_human_name() -> str:
    random_index = random.randint(1, 4)
    #random_index = random.randint(1, len(g_active_user_dict)-1)
    return g_human_names[random_index]


def init_state(w3: Web3, file_path: str, skip_import_keys: bool):
    global g_address_list, g_address_dict, g_names_pubkey_dict
    with open(file_path,'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            curr_human_name = line[0]
            curr_private_key = line[1]
            curr_address = line[2]
            g_address_list.append(line[2])
            if not skip_import_keys:
                try:
                    success = w3.geth.personal.import_raw_key(curr_private_key, '')
                    logging.debug('Imported prefunded key {} {}'.format(curr_human_name, success))
                except ValueError as e:
                    if e.args[0]['code'] == -32000 and e.args[0]['message'] == 'account already exists':
                        logging.info('Key already imported {}'.format(curr_human_name))
                    else:
                        raise e
            success_a = w3.geth.personal.unlock_account(ChecksumAddress(HexAddress(HexStr(curr_address))), '', 0)
            if not success_a:
                raise RuntimeError('Do you not know your own bloody test passwords?!')
            curr_balance = w3.eth.getBalance(curr_address)
            curr_addr = Address({
                'human_name': curr_human_name,
                'private_key': curr_private_key,
                'addr': curr_address,
                'balance': curr_balance,
                'balance_start': curr_balance})
            logging.info('{}: {}'.format(curr_addr['human_name'],curr_addr['balance']))
            g_names_pubkey_dict[curr_addr['human_name']] = curr_addr['addr']
            g_address_dict[curr_addr['addr']] = curr_addr
        gethMiner = GethMiner(w3)
        gethMiner.start(1)


def deploy_contract(w3: Web3, file_path_compile: str, file_path_abi: str):
    global g_forsage_contract
    with open(file_path_compile, 'r') as f:
        jo = json.loads(f.read())
        compiled_contract = jo['object']
        with open(file_path_abi, 'r') as f2:
            abi = json.loads(f2.read())
            ForsageContract = w3.eth.contract(abi=abi, bytecode=compiled_contract)
            constructor_data = ForsageContract.constructor(g_names_pubkey_dict['alpha']).buildTransaction(
                    {'from': g_names_pubkey_dict['alpha'], 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI})
            #constructor_data = ForsageContract.constructor('0xAD0e6fA4C381A845da31ff52721A4531769F7582').buildTransaction(
            #        {'from': '0xAD0e6fA4C381A845da31ff52721A4531769F7582', 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI})
            tx_hash_constructor = w3.eth.sendTransaction(constructor_data)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash_constructor)
            c_addr = tx_receipt['contractAddress']
            g_forsage_contract = w3.eth.contract(address=c_addr, abi=abi)
            logging.info('forsage instantiated contract_address {}'.format(g_forsage_contract.address))

def unlock_test_accounts(w3: Web3):
    for name in g_human_names:
        address = g_names_pubkey_dict[name]
        success = w3.geth.personal.unlock_account(ChecksumAddress(HexAddress(HexStr(address))), '', 0)
        if not success:
            raise RuntimeError('Do you not know your own bloody test passwords?!')

def compute_print_balance_delta(past_active_user_dict: Dict[str, User]):
    for name in g_human_names:
        if name not in g_active_user_dict and name not in past_active_user_dict:
            continue # no change, user didn't exist before and they dont now, delta=0
        elif name in g_active_user_dict and name not in past_active_user_dict:
            out_wei = g_active_user_dict[name]['balanceDelta'].get()
            out_eth = '{:f}'.format(wei_to_eth(out_wei)).rstrip('0')
            print('Balance Change: New user {} {}'.format(name, out_eth))
        elif name not in g_active_user_dict and name in past_active_user_dict:
            raise RuntimeError('Users should never be removed from Forsage')
        else: # k both exist
            _delta = g_active_user_dict[name]['balanceDelta'].get() - past_active_user_dict[name]['balanceDelta'].get()
            _delta2 = g_active_user_dict[name]['balanceLastChange']
            if _delta2 != _delta:
                logging.warning(
                        'Last state change calculation in collect_state was done incorrectly! {} {} {}'.format(
                            name, _delta, _delta2))
            if _delta == 0:
                continue
            out_eth = '{:f}'.format(wei_to_eth(_delta)).rstrip('0')
            print('Balance Change: {} {}'.format(name, out_eth))

def conditional_print(in_string: str, condition: bool):
    if condition:
        print(in_string)

def compute_print_delta(past_active_user_dict: Dict[str, User], do_print: bool) -> Set[int]:
    new_stuff = set()
    for name in g_human_names:
        if name not in g_active_user_dict and name not in past_active_user_dict:
            continue # no change, user didn't exist before and they dont now, delta=0
        elif name in g_active_user_dict and name not in past_active_user_dict:
            conditional_print('NEW USER ADDED TO FORSAGE', do_print)
            new_user = g_active_user_dict[name]
            if do_print:
                print_user_state(new_user)
            new_stuff.add(id(new_user['name']))
            new_stuff.add(id(new_user['id']))
            new_stuff.add(id(new_user['referrer']))
            new_stuff.add(id(new_user['partnersCount']))
            for level in new_user['x3Matrix']:
                if level is not None:
                    new_stuff.add(id(level))
                    new_stuff.add(id(level['currentReferrer']))
                    new_stuff.add(id(level['blocked']))
            for level6 in new_user['x6Matrix']:
                if level6 is not None:
                    new_stuff.add(id(level6))
                    new_stuff.add(id(level6['currentReferrer']))
                    new_stuff.add(id(level6['blocked']))
                    new_stuff.add(id(level6['closedPart']))
            new_stuff.add(id(new_user['balanceDelta']))
        elif name not in g_active_user_dict and name in past_active_user_dict:
            raise RuntimeError('Users should never be removed from Forsage')
        else: # both exist, now check each element of each user
            curr = past_active_user_dict[name]
            future = g_active_user_dict[name]
            if not (curr['name'] == future['name'] and curr['name'] == name):
                raise RuntimeError('Users should never be able to change their names')
            if curr['id'] != future['id']:
                # This case shouldn't be possible either, but we'll allow for it anyway
                conditional_print('DIFF ID {}: OLD {} | New {}'.format(name, curr['id'], future['id']), do_print)
                new_stuff.add(id(future['id']))
            if curr['referrer'] != future['referrer']:
                conditional_print('DIFF REFERRER {}: OLD {} | New {}'.format(name, curr['referrer'], future['referrer']), do_print)
                new_stuff.add(id(future['referrer']))
            if curr['partnersCount'] != future['partnersCount']:
                conditional_print('DIFF PARTNER COUNT {}: OLD {} | NEW {}'.format(name, curr['partnersCount'], future['partnersCount']), do_print)
                new_stuff.add(id(future['partnersCount']))
            if curr['balanceDelta'] != future['balanceDelta']:
                conditional_print('DIFF BALANCE DELTA {}: OLD {:g} | NEW {:g}'.format(name, wei_to_eth(curr['balanceDelta'].get()), wei_to_eth(future['balanceDelta'].get())), do_print)
                new_stuff.add(id(future['balanceDelta']))
            for i in range(0, 12):
                left_a3 = curr['activeX3Levels'][i]
                right_a3 = future['activeX3Levels'][i]
                if left_a3 != right_a3:
                    conditional_print('DIFF ACTIVE X3 LEVEL {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, left_a3, right_a3), do_print)
                    new_stuff.add(id(right_a3))

                left_m3 = curr['x3Matrix'][i]
                left_blocked: Optional[MutableBool] = None
                left_current_referrer: Optional[MutableString] = None
                left_referrals: Optional[List[MutableString]] = None
                if left_m3 is not None:
                    left_blocked = left_m3['blocked']
                    left_current_referrer = left_m3['currentReferrer']
                    left_referrals = left_m3['referrals']

                right_m3 = future['x3Matrix'][i]
                right_blocked: Optional[MutableBool] = None
                right_current_referrer: Optional[MutableString] = None
                right_referrals: Optional[List[MutableString]] = None
                if right_m3 is not None:
                    right_blocked = right_m3['blocked']
                    right_current_referrer = right_m3['currentReferrer']
                    right_referrals = right_m3['referrals']
                if left_blocked != right_blocked:
                    conditional_print('DIFF X3 BLOCKED {}: INDEX {} OLD {} | NEW {}'.format(
                        name,
                        i,
                        left_blocked,
                        right_blocked), do_print)
                    new_stuff.add(id(right_blocked))
                if left_current_referrer != right_current_referrer:
                    conditional_print('DIFF X3 REFERRER {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, left_current_referrer, right_current_referrer), do_print)
                    new_stuff.add(id(right_current_referrer))
                len_left_referrals = 0
                if left_referrals is not None:
                    len_left_referrals = len(left_referrals)
                len_right_referrals = 0
                if right_referrals is not None:
                    len_right_referrals = len(right_referrals)
                if len_left_referrals != len_right_referrals:
                    conditional_print('DIFF X3 REFERRALS LEN {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, len_left_referrals, len_right_referrals), do_print)
                if len_left_referrals > len_right_referrals:
                    max_referrals_list_len = len_left_referrals
                else:
                    max_referrals_list_len = len_right_referrals

                for j in range(0, max_referrals_list_len):
                    left_referral_j = None
                    if left_referrals:
                        if j < len_left_referrals:
                            left_referral_j = left_referrals[j]
                    right_referral_j = None
                    if right_referrals:
                        if j < len_right_referrals:
                            right_referral_j = right_referrals[j]
                    if left_referral_j != right_referral_j:
                        conditional_print('DIFF X3 {} INDEX INTO MATRIX {} REFERRALS LIST INDEX {} OLD {} | NEW {}'.format(
                            name, i, j, left_referral_j, right_referral_j), do_print)
                        new_stuff.add(id(right_referral_j))

                left_a6 = curr['activeX6Levels'][i]
                right_a6 = future['activeX6Levels'][i]
                if left_a6 != right_a6:
                    conditional_print('DIFF ACTIVE X6 LEVEL {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, left_a6, right_a6), do_print)
                    new_stuff.add(id(right_a6))


                left_m6 = curr['x6Matrix'][i]
                right_m6 = future['x6Matrix'][i]

                left_m6_blocked: Optional[MutableBool] = None
                left_m6_current_referrer: Optional[MutableString] = None
                left_m6_first_level_referrals: Optional[List[MutableString]] = None
                left_m6_second_level_referrals: Optional[List[MutableString]] = None
                left_m6_closed_part: Optional[MutableString] = None
                if left_m6 is not None:
                    left_m6_blocked = left_m6['blocked']
                    left_m6_current_referrer = left_m6['currentReferrer']
                    left_m6_first_level_referrals = left_m6['firstLevelReferrals']
                    left_m6_second_level_referrals = left_m6['secondLevelReferrals']
                    left_m6_closed_part = left_m6['closedPart']

                right_m6_blocked: Optional[MutableBool] = None
                right_m6_current_referrer: Optional[MutableString] = None
                right_m6_first_level_referrals: Optional[List[MutableString]] = None
                right_m6_second_level_referrals: Optional[List[MutableString]] = None
                right_m6_closed_part: Optional[MutableString] = None
                if right_m6 is not None:
                    right_m6_blocked = right_m6['blocked']
                    right_m6_current_referrer = right_m6['currentReferrer']
                    right_m6_first_level_referrals = right_m6['firstLevelReferrals']
                    right_m6_second_level_referrals = right_m6['secondLevelReferrals']
                    right_m6_closed_part = right_m6['closedPart']

                if left_m6_blocked != right_m6_blocked:
                    conditional_print('DIFF X6 BLOCKED {}: INDEX {} OLD {} | NEW {}'.format(
                        name,
                        i,
                        left_m6_blocked,
                        right_m6_blocked), do_print)
                    new_stuff.add(id(right_m6_blocked))
                if left_m6_current_referrer != right_m6_current_referrer:
                    conditional_print('DIFF X6 REFERRER {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, left_m6_current_referrer, right_m6_current_referrer), do_print)
                    new_stuff.add(id(right_m6_current_referrer))
                if left_m6_closed_part != right_m6_closed_part:
                    conditional_print('DIFF X6 CLOSED PART {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, left_m6_closed_part, right_m6_closed_part), do_print)
                    new_stuff.add(id(right_m6_closed_part))

                len_left_m6_first_level_referrals = 0
                if left_m6_first_level_referrals is not None:
                    len_left_m6_first_level_referrals = len(left_m6_first_level_referrals)
                len_right_m6_first_level_referrals = 0
                if right_m6_first_level_referrals is not None:
                    len_right_m6_first_level_referrals = len(right_m6_first_level_referrals)
                if len_left_m6_first_level_referrals != len_right_m6_first_level_referrals:
                    conditional_print('DIFF X6 FIRSTLIST REFERRALS LEN {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, len_left_m6_first_level_referrals, len_right_m6_first_level_referrals), do_print)
                    new_stuff.add(id(len_right_m6_first_level_referrals))
                if len_left_m6_first_level_referrals > len_right_m6_first_level_referrals:
                    max_first_level_referrals_list_len = len_left_m6_first_level_referrals
                else:
                    max_first_level_referrals_list_len = len_right_m6_first_level_referrals

                for j in range(0, max_first_level_referrals_list_len):
                    left_m6_first_level_referral_j = None
                    if left_m6_first_level_referrals:
                        if j < len_left_m6_first_level_referrals:
                            left_m6_first_level_referral_j = left_m6_first_level_referrals[j]
                    right_m6_first_level_referral_j = None
                    if right_m6_first_level_referrals:
                        if j < len_right_m6_first_level_referrals:
                            right_m6_first_level_referral_j = right_m6_first_level_referrals[j]
                    if left_m6_first_level_referral_j != right_m6_first_level_referral_j:
                        conditional_print('DIFF X6 {} INDEX INTO MATRIX {} REFERRALS LIST INDEX {} OLD {} | NEW {}'.format(
                            name, i, j, left_m6_first_level_referral_j, right_m6_first_level_referral_j), do_print)
                        new_stuff.add(id(right_m6_first_level_referral_j))

                len_left_m6_second_level_referrals = 0
                if left_m6_second_level_referrals is not None:
                    len_left_m6_second_level_referrals = len(left_m6_second_level_referrals)
                len_right_m6_second_level_referrals = 0
                if right_m6_second_level_referrals is not None:
                    len_right_m6_second_level_referrals = len(right_m6_second_level_referrals)
                if len_left_m6_second_level_referrals != len_right_m6_second_level_referrals:
                    conditional_print('DIFF X6 SECONDLIST REFERRALS LEN {}: INDEX {} OLD {} | NEW {}'.format(
                        name, i, len_left_m6_second_level_referrals, len_right_m6_second_level_referrals), do_print)
                    new_stuff.add(id(len_right_m6_second_level_referrals))
                if len_left_m6_second_level_referrals > len_right_m6_second_level_referrals:
                    max_second_level_referrals_list_len = len_left_m6_second_level_referrals
                else:
                    max_second_level_referrals_list_len = len_right_m6_second_level_referrals

                for j in range(0, max_second_level_referrals_list_len):
                    left_m6_second_level_referral_j = None
                    if left_m6_second_level_referrals:
                        if j < len_left_m6_second_level_referrals:
                            left_m6_second_level_referral_j = left_m6_second_level_referrals[j]
                    right_m6_second_level_referral_j = None
                    if right_m6_second_level_referrals:
                        if j < len_right_m6_second_level_referrals:
                            right_m6_second_level_referral_j = right_m6_second_level_referrals[j]
                    if left_m6_second_level_referral_j != right_m6_second_level_referral_j:
                        conditional_print('DIFF X6 SECONDLIST {} INDEX INTO MATRIX {} REFERRALS LIST INDEX {} OLD {} | NEW {}'.format(
                            name, i, j, left_m6_second_level_referral_j, right_m6_second_level_referral_j), do_print)
                        new_stuff.add(id(right_m6_second_level_referral_j))
    conditional_print('+++++++++++++++++++++++++++++++++++++++++++', do_print)
    return new_stuff


def print_user_state(user: User):
    pp = pprint.PrettyPrinter(indent=4)
    print('Name: ', user['name'])
    print('Net Balance interaction: {0:g}'.format(wei_to_eth(user['balanceDelta'].get())))
    print('Referrer: ', user['referrer'])
    print('Forsage ID & Partners Count: {} {}'.format(user['id'], user['partnersCount']))
    print('Active X3 Levels:')
    print(user['activeX3Levels'])
    pp.pprint(user['x3Matrix'])
    print('Active X6 Levels:')
    print(user['activeX6Levels'])
    pp.pprint(user['x6Matrix'])
    print('-------------------------------------------')


def collect_state_snapshot(w3: Web3):
    """Collects state snapshot and overwrites global state in g_active_user_dict. Returns old state to caller."""
    global g_active_user_dict
    l_active_user_dict: Dict[str, User] = {}
    if g_forsage_contract:
        for name in g_human_names:
            address = g_names_pubkey_dict[name]
            if g_forsage_contract.functions.isUserExists(address).call():
                result = g_forsage_contract.functions.users(address).call()
                user_id = result[0]
                user_referrer = g_address_dict[result[1]]['human_name']
                user_partners_count = result[2]
                user_active_x3_levels = []
                user_active_x6_levels = []
                user_x3_matrices: List[Optional[X3]] = []
                user_x6_matrices: List[Optional[X6]] = []
                for i in range(1, 13):
                    activeX3Level = g_forsage_contract.functions.usersActiveX3Levels(address, i).call()
                    activeX6Level = g_forsage_contract.functions.usersActiveX6Levels(address, i).call()
                    user_active_x3_levels.append(activeX3Level)
                    user_active_x6_levels.append(activeX6Level)
                    if activeX3Level:
                        x3Matrix = g_forsage_contract.functions.usersX3Matrix(address, i).call()
                        x3Matrix_current_referrer = g_address_dict[x3Matrix[0]]['human_name']
                        x3Matrix_referrals = []
                        for ref_addr in x3Matrix[1]:
                            x3Matrix_referrals.append(MutableString(g_address_dict[ref_addr]['human_name']))
                        x3Matrix_blocked = MutableBool(bool(x3Matrix[2]))
                        current_x3 = X3({ 'currentReferrer': MutableString(x3Matrix_current_referrer), 'referrals': x3Matrix_referrals, 'blocked': x3Matrix_blocked })
                        user_x3_matrices.append(current_x3)
                    else:
                        user_x3_matrices.append(None)

                    if activeX6Level:
                        x6Matrix = g_forsage_contract.functions.usersX6Matrix(address, i).call()
                        x6Matrix_current_referrer = g_address_dict[x6Matrix[0]]['human_name']
                        x6Matrix_blocked = MutableBool(bool(x6Matrix[3]))
                        x6Matrix_closed_part = MutableString(g_address_dict[x6Matrix[4]]['human_name'])
                        x6Matrix_first_level_referrals = []
                        x6Matrix_second_level_referrals = []
                        for ref_addr in x6Matrix[1]:
                            x6Matrix_first_level_referrals.append(MutableString(g_address_dict[ref_addr]['human_name']))
                        for ref_addr in x6Matrix[2]:
                            x6Matrix_second_level_referrals.append(MutableString(g_address_dict[ref_addr]['human_name']))
                        current_x6 = X6({ 'currentReferrer': MutableString(x6Matrix_current_referrer), 'firstLevelReferrals': x6Matrix_first_level_referrals, 'secondLevelReferrals': x6Matrix_second_level_referrals, 'blocked': x6Matrix_blocked, 'closedPart': x6Matrix_closed_part})
                        user_x6_matrices.append(current_x6)
                    else:
                        user_x6_matrices.append(None)

                curr_balance = int(w3.eth.getBalance(address))
                start_balance = g_address_dict[address]['balance_start']
                delta_balance = curr_balance - start_balance
                try:
                    state_change_delta = delta_balance - g_active_user_dict[name]['balanceDelta'].get()
                    if g_active_user_dict[name]['balanceDelta'] !=  delta_balance:
                        logging.info('state change delta {} {} {}'.format(name, g_active_user_dict[name]['balanceDelta'], delta_balance))
                except KeyError:
                    state_change_delta = delta_balance

                user = User({
                            'name': MutableString(name),
                            'id': MutableInt(user_id),
                            'referrer': MutableString(user_referrer),
                            'partnersCount': MutableInt(user_partners_count),
                            'activeX3Levels': user_active_x3_levels,
                            'activeX6Levels': user_active_x6_levels,
                            'x3Matrix': user_x3_matrices,
                            'x6Matrix': user_x6_matrices,
                            'balanceDelta': MutableInt(delta_balance),
                            'balanceLastChange': state_change_delta
                        })
                l_active_user_dict[name] = user

    else:
        raise RuntimeError('Forsage contract must be deployed to collect state')

    old_active_user_dict = g_active_user_dict
    g_active_user_dict = l_active_user_dict
    return old_active_user_dict

def print_new_user_place_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['user']
            user_str = g_address_dict[str(user)]['human_name']
            referrer = args['referrer']
            referrer_str = g_address_dict[str(referrer)]['human_name']
            matrix = args['matrix']
            if int(matrix) == 1:
                matrix_str = 'X3'
            elif int(matrix) == 2:
                matrix_str = 'X6'
            else:
                raise RuntimeError('Matrix invalid {}'.format(matrix))
            level = args['level']
            place = args['place']
            out_str = '{}: {} under {} {} level {} place {}'.format(event_name, user_str, referrer_str, matrix_str, level, place)
            conditional_print(out_str, True)

def print_registration_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['user']
            user_str = g_address_dict[str(user)]['human_name']
            referrer = args['referrer']
            referrer_str = g_address_dict[str(referrer)]['human_name']
            out_str = '{}: {} referred by {}'.format(event_name, user_str, referrer_str)
            conditional_print(out_str, True)

def print_upgrade_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['user']
            user_str = g_address_dict[str(user)]['human_name']
            referrer = args['referrer']
            referrer_str = g_address_dict[str(referrer)]['human_name']
            matrix = args['matrix']
            if int(matrix) == 1:
                matrix_str = 'X3'
            elif int(matrix) == 2:
                matrix_str = 'X6'
            else:
                raise RuntimeError('Matrix invalid {}'.format(matrix))
            level = args['level']
            out_str = '{}: {} referred by {} {} upgrade level {}'.format(event_name, user_str, referrer_str, matrix_str, level)
            conditional_print(out_str, True)

def print_reinvest_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['user']
            user_str = g_address_dict[str(user)]['human_name']
            referrer = args['currentReferrer']
            referrer_str = g_address_dict[str(referrer)]['human_name']
            matrix = args['matrix']
            if int(matrix) == 1:
                matrix_str = 'X3'
            elif int(matrix) == 2:
                matrix_str = 'X6'
            else:
                raise RuntimeError('Matrix invalid {}'.format(matrix))
            level = args['level']
            caller = args['caller']
            caller_str = g_address_dict[str(caller)]['human_name']
            out_str = '{}: {} reinvested by {} called by {} {} reinvest level {}'.format(event_name, user_str, referrer_str, caller_str, matrix_str, level)
            conditional_print(out_str, True)

def print_extra_eth_divs_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['from']
            user_str = g_address_dict[str(user)]['human_name']
            receiver = args['receiver']
            receiver_str = g_address_dict[str(receiver)]['human_name']
            matrix = args['matrix']
            if int(matrix) == 1:
                matrix_str = 'X3'
            elif int(matrix) == 2:
                matrix_str = 'X6'
            else:
                raise RuntimeError('Matrix invalid {}'.format(matrix))
            level = args['level']
            out_str = '{}: from {} to {} {} ExtraDivs level {}'.format(event_name, user_str, receiver_str, matrix_str, level)
            conditional_print(out_str, True)

def print_missed_eth_log(rich_logs: List[Dict], do_print: bool):
    if do_print:
        for item in rich_logs:
            event_name = item['event']
            args = item['args']
            user = args['from']
            user_str = g_address_dict[str(user)]['human_name']
            receiver = args['receiver']
            receiver_str = g_address_dict[str(receiver)]['human_name']
            matrix = args['matrix']
            if int(matrix) == 1:
                matrix_str = 'X3'
            elif int(matrix) == 2:
                matrix_str = 'X6'
            else:
                raise RuntimeError('Matrix invalid {}'.format(matrix))
            level = args['level']
            out_str = '{}: from {} to {} {} MissedETH level {}'.format(event_name, user_str, receiver_str, matrix_str, level)
            conditional_print(out_str, True)


def print_event_logs(tx_reciept: TxReceipt, do_print: bool):
    assert g_forsage_contract is not None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rich_logs = g_forsage_contract.events.NewUserPlace().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_new_user_place_log(rich_logs, do_print)
        rich_logs = g_forsage_contract.events.MissedEthReceive().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_missed_eth_log(rich_logs, do_print)
        rich_logs = g_forsage_contract.events.SentExtraEthDividends().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_extra_eth_divs_log(rich_logs, do_print)
        rich_logs = g_forsage_contract.events.Reinvest().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_reinvest_log(rich_logs, do_print)
        rich_logs = g_forsage_contract.events.Upgrade().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_upgrade_log(rich_logs, do_print)
        rich_logs = g_forsage_contract.events.Registration().processReceipt(tx_receipt)
        if len(rich_logs) != 0:
            print_registration_log(rich_logs, do_print)



def dump_full_state(state_dict: Dict[str, User]):
    for name in g_human_names:
        try:
            print_user_state(state_dict[name])
        except KeyError:
            continue

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # control verbosity
    w3 = Web3(Web3.IPCProvider('forsagetestdata/forsage_geth.ipc'))
    init_state(w3, 'test_addresses.csv', True)
    deploy_contract(w3, 'forsage_compiled.json', 'forsage_abi.json')
    if not g_forsage_contract:
        raise RuntimeError('Forsage contract must be deployed to run tests')

    collect_state_snapshot(w3)
    print('Bravo registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['alpha']).transact(
            {'from': g_names_pubkey_dict['bravo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #dump_full_state(g_active_user_dict)
    delta_items = compute_print_delta(prev_state, False)
    #graph_full_state('statepngs/001_bravo_register', 'Bravo Registers', g_active_user_dict, g_human_names)
    #graph_full_state_per_user('statepngs/001_bravo_register', g_active_user_dict, g_human_names, delta_items)
    graph_full_state_per_user('statepngs/201_bravo_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Charlie Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['charlie'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_charlie_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    # print('Bravo Buys New x3 Level')
    # tx_receipt = w3.eth.waitForTransactionReceipt(
    #         g_forsage_contract.functions.buyNewLevel(1,2).transact(
    #         {'from': g_names_pubkey_dict['bravo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    # ))

    # if tx_receipt['status'] != 1:
    #     raise RuntimeError('Error with TX check require statements\n\n{}'.format(str(tx_receipt)))
    # prev_state = collect_state_snapshot(w3)
    # compute_print_balance_delta(prev_state)
    # delta_items = compute_print_delta(prev_state, False)
    # graph_full_state_per_user('statepngs/201_bravo_buy_new_level_x3', g_active_user_dict, g_human_names, delta_items)
    # print_event_logs(tx_receipt, True)

    print('Delta Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['delta'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #graph_full_state('statepngs/004_delta_register', 'Delta Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_delta_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Echo Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['echo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #graph_full_state('statepngs/005_echo_register', 'Echo Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_echo_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Foxtrot Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['foxtrot'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #graph_full_state('statepngs/006_foxtrot_register', 'Foxtrot Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_foxtrot_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Golf Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['golf'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #dump_full_state(g_active_user_dict)
    #graph_full_state('statepngs/007_golf_register', 'Golf Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_golf_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Hotel Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['hotel'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #dump_full_state(g_active_user_dict)
    #graph_full_state('statepngs/008_hotel_register', 'Hotel Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_hotel_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('India Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['india'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    #dump_full_state(g_active_user_dict)
    #graph_full_state('statepngs/009_india_register', 'India Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_india_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Juliet Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['juliet'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    #compute_print_balance_delta(prev_state)
    #dump_full_state(g_active_user_dict)
    #graph_full_state('statepngs/010_juliet_register', 'Juliet Registers', g_active_user_dict, g_human_names)
    graph_full_state_per_user('statepngs/201_juliet_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Bravo Buys New x6 Level')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.buyNewLevel(2,2).transact(
            {'from': g_names_pubkey_dict['bravo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))

    if tx_receipt['status'] != 1:
        raise RuntimeError('Error with TX check require statements\n\n{}'.format(str(tx_receipt)))
    prev_state = collect_state_snapshot(w3)
    delta_items = compute_print_delta(prev_state, False)
    compute_print_balance_delta(prev_state)
    #graph_full_state_per_user('statepngs/102_bravo_buy_new_level', g_active_user_dict, g_human_names, delta_items)
    graph_full_state_per_user('statepngs/201_bravo_buy_new_level_x6', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Kilo Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['charlie']).transact(
            {'from': g_names_pubkey_dict['kilo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_kilo_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Lima Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['alpha']).transact(
            {'from': g_names_pubkey_dict['lima'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_lima_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Mike Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['alpha']).transact(
            {'from': g_names_pubkey_dict['mike'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_mike_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('November Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['delta']).transact(
            {'from': g_names_pubkey_dict['november'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_november_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Oscar Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['oscar'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_oscar_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Papa Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['alpha']).transact(
            {'from': g_names_pubkey_dict['papa'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_papa_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Quebec Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['quebec'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_quebec_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Romeo Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['bravo']).transact(
            {'from': g_names_pubkey_dict['romeo'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_romeo_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Charlie Buys New x6 Level')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.buyNewLevel(2,2).transact(
            {'from': g_names_pubkey_dict['charlie'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_charlie_buy_new_x6', g_active_user_dict, g_human_names, delta_items)


    print('Sierra Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['charlie']).transact(
            {'from': g_names_pubkey_dict['sierra'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_sierra_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)
    print_event_logs(tx_receipt, True)

    print('Tango Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['sierra']).transact(
            {'from': g_names_pubkey_dict['tango'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_tango_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Uniform Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['sierra']).transact(
            {'from': g_names_pubkey_dict['uniform'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_uniform_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Victor Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['sierra']).transact(
            {'from': g_names_pubkey_dict['victor'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_victor_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Whiskey Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['sierra']).transact(
            {'from': g_names_pubkey_dict['whiskey'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_whiskey_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print('Xray Registers')
    tx_receipt = w3.eth.waitForTransactionReceipt(
            g_forsage_contract.functions.registrationExt(g_names_pubkey_dict['kilo']).transact(
            {'from': g_names_pubkey_dict['xray'], 'value': eth_to_Wei(0.05), 'gas':  GAS_MAX, 'gasPrice': ONE_GWEI}
    ))
    prev_state = collect_state_snapshot(w3)
    compute_print_balance_delta(prev_state)
    delta_items = compute_print_delta(prev_state, False)
    graph_full_state_per_user('statepngs/201_xray_register', g_active_user_dict, g_human_names, delta_items)
    print_event_logs(tx_receipt, True)

    print()
    print('Done.')

