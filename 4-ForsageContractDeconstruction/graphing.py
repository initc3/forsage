#!/usr/bin/env python3

__author__ = 'tyler'

from graphviz import Graph
from typing import Dict, Tuple, List, Set
from expiriment_constants import Address, X3, X6, User, wei_to_eth, MutableString, MutableBool, MutableInt
import logging


def construct_concise_label(user: User, new_items_id_set: Set[int]) -> str:
    name = user['name']
    if id(name) in new_items_id_set:
        name_str = '<font color="blue">{}</font>'.format(name.get())
    else:
        name_str = name.get()

    balance_last_change = user['balanceLastChange']
    full_bal_history = user['balanceDelta']
    if id(full_bal_history) in new_items_id_set:
        full_bal_str = r'<br/><font color="blue">FullBal: {:f}</font>'.format(wei_to_eth(full_bal_history.get()))
    else:
        full_bal_str = r'<br/>FullBal: {:f}'.format(wei_to_eth(full_bal_history.get()))
    if balance_last_change != 0:
        if balance_last_change > 0:
            tmp = '{:f}'.format(wei_to_eth(balance_last_change)).rstrip('0')
            delta_balance = '<font color="forestgreen">{}</font>'.format(tmp)
        elif balance_last_change < 0:
            tmp = '{:f}'.format(wei_to_eth(balance_last_change)).rstrip('0')
            delta_balance = '<font color="red">{}</font>'.format(tmp)
        # + f_id_str
        label = r'<' + name_str + full_bal_str + r'<br/><font color="blue">Δ_Bal:</font>' + delta_balance + r'>'
    else:
        # + f_id_str
        label = r'<' + name_str + full_bal_str + r'<br/>Δ_Bal: 0' + r'>'
    return label


def construct_full_label(user: User, new_items_id_set: Set[int]) -> str:
    name = user['name']
    if id(name) in new_items_id_set:
        name_str = '<font color="blue">{}</font>'.format(name.get())
    else:
        name_str = name.get()
    parent = user['referrer']
    if id(parent) in new_items_id_set:
        parent_str = '<br/><font color="blue">referrer: {}</font>'.format(parent.get())
    else:
        parent_str = r'<br/>referrer: {}'.format(parent.get())
    balance_last_change = user['balanceLastChange']
    num_partners = user['partnersCount']
    if id(num_partners) in new_items_id_set:
        num_partners_str = r'<font color="blue"><br/>Partners:' + '{}</font>'.format(num_partners)
    else:
        num_partners_str = r'<br/>Partners: ' + str(num_partners)
    full_bal_history = user['balanceDelta']
    if id(full_bal_history) in new_items_id_set:
        full_bal_str = r'<br/><font color="blue">FullBal: {:f}</font>'.format(wei_to_eth(full_bal_history.get()))
    else:
        full_bal_str = r'<br/>FullBal: {:f}'.format(wei_to_eth(full_bal_history.get()))
    if balance_last_change != 0:
        if balance_last_change > 0:
            tmp = '{:f}'.format(wei_to_eth(balance_last_change)).rstrip('0')
            delta_balance = '<font color="forestgreen">{}</font>'.format(tmp)
        elif balance_last_change < 0:
            tmp = '{:f}'.format(wei_to_eth(balance_last_change)).rstrip('0')
            delta_balance = '<font color="red">{}</font>'.format(tmp)
        # + f_id_str
        label = r'<' + name_str + parent_str + num_partners_str + full_bal_str + r'<br/><font color="blue">Δ_Bal:</font>' + delta_balance + r'>'
    else:
        # + f_id_str
        label = r'<' + name_str + parent_str + num_partners_str + full_bal_str + r'<br/>Δ_Bal: 0' + r'>'
    return label

def generate_graph_user_state(user: User, all_user_dict: Dict[str, User], make_cluster_name: bool, new_items_id_set: Set[int]) -> Tuple[Graph, Graph]:
    title_x3 = user['name'].get() + '_X3'
    title_x6 = user['name'].get() + '_X4'
    if make_cluster_name:
        dot_x3 = Graph(name='cluster_' + title_x3)
        dot_x6 = Graph(name='cluster_' + title_x6)
    else:
        dot_x3 = Graph(format='pdf')
        dot_x6 = Graph(format='pdf')
    dot_x3.attr(label=title_x3, labelloc = 't')
    dot_x6.attr(label=title_x6, labelloc = 't')
    user_label = construct_full_label(user, new_items_id_set)
    logging.debug('User: ', title_x3)
    logging.debug('label: ', user_label)
    if id(user['name']) in new_items_id_set and id(user['id']) in new_items_id_set:
        dot_x3.node('user' + title_x3, user_label, color="blue")
        dot_x6.node('user' + title_x6, user_label, color="blue")
    else:
        dot_x3.node('user' + title_x3, user_label)
        dot_x6.node('user' + title_x6, user_label)
    # ok I used to graph the parent with the current user but now I think that
    # you can just check the parent's pdf
    # parent = user['referrer'].get()
    # # special corner case alpha has no parent
    # if parent == '0x0':
    #     dot_x3.node('parent' + title_x3, '0x0')
    #     dot_x6.node('parent' + title_x6, '0x0')
    # else:
    #     parent_user = all_user_dict[parent]
    #     parent_label = construct_label(parent_user, new_items_id_set)
    #     dot_x3.node('parent' + title_x3, parent_label)
    #     dot_x6.node('parent' + title_x6, parent_label)
    # dot_x3.edge('parent' + title_x3, 'user' + title_x3)
    # dot_x6.edge('parent' + title_x6, 'user' + title_x6)
    for index in range(0, len(user['activeX3Levels'])):
        level_exists = user['activeX3Levels'][index]
        level_node_name = title_x3 + '_x3_' + str(index)
        if level_exists:
            x3Matrix_element = user['x3Matrix'][index]
            if x3Matrix_element is None:
                raise RuntimeError('activeX3Levels MUST match x3Matrix')
            else:
                if id(x3Matrix_element['currentReferrer']) in new_items_id_set:
                    level_referrer = r'<font color="blue">r: ' + str(x3Matrix_element['currentReferrer']) + r'</font>'
                else:
                    level_referrer = r'r: ' + str(x3Matrix_element['currentReferrer'])
                if id(x3Matrix_element['blocked']) in new_items_id_set:
                    level_blocked =  r'<br/><font color="blue">b: ' + str(x3Matrix_element['blocked']) + r'</font>'
                else:
                    level_blocked =  r'<br/>b: ' + str(x3Matrix_element['blocked'])
                level_xlabel = r'<' + level_referrer + level_blocked + r'>'
                if id(x3Matrix_element['blocked']) in new_items_id_set and id(x3Matrix_element['currentReferrer']) in new_items_id_set:
                    level_node = dot_x3.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box',
                                         color='blue')
                elif str(x3Matrix_element['blocked']) == 'True':
                    level_node = dot_x3.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box',
                                         color='red')
                else:
                    level_node = dot_x3.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box')
                referrals = x3Matrix_element['referrals']
                for index_2 in range(0, len(referrals)):
                    referral = referrals[index_2].get()
                    referral_label = construct_concise_label(all_user_dict[referral], new_items_id_set)
                    referral_graph_name = level_node_name + referral + str(index_2)
                    if id(all_user_dict[referral]['name']) in new_items_id_set and id(all_user_dict[referral]['id']) in new_items_id_set:
                        dot_x3.node(referral_graph_name, referral_label, color="blue")
                    else:
                        dot_x3.node(referral_graph_name, referral_label)
                    dot_x3.edge(level_node_name, referral_graph_name)

        else:
            if id(user['name']) in new_items_id_set and id(user['id']) in new_items_id_set:
                level_node = dot_x3.node(level_node_name, '', shape='point', color="blue")
                #level_node = dot_x3.node(level_node_name,  r'<' +'<font color="blue">x</font>' + r'>', shape='plain', color="blue")
            else:
                level_node = dot_x3.node(level_node_name, '', shape='point')
                #level_node = dot_x3.node(level_node_name, r'<' +'<font color="red">x</font>' + r'>', shape='plain')
        dot_x3.edge('user' + title_x3, level_node_name)

    for index in range(0, len(user['activeX6Levels'])):
        level_exists = user['activeX6Levels'][index]
        level_node_name = title_x6 + '_x6_' + str(index)
        if level_exists:
            x6Matrix_element = user['x6Matrix'][index]
            if x6Matrix_element is None:
                raise RuntimeError('activeX6Levels MUST match x6Matrix')
            else:
                if id(x6Matrix_element['currentReferrer']) in new_items_id_set:
                    level_referrer = '<font color="blue">r: ' + x6Matrix_element['currentReferrer'].get() + '</font>'
                else:
                    level_referrer = 'r: ' + x6Matrix_element['currentReferrer'].get()
                if id(x6Matrix_element['blocked']) in new_items_id_set:
                    level_blocked =  r'<br/><font color="blue">b: ' + str(x6Matrix_element['blocked']) + r'</font>'
                else:
                    level_blocked =  r'<br/>b: ' + str(x6Matrix_element['blocked'])
                if id(x6Matrix_element['closedPart']) in new_items_id_set:
                    level_closedPart =  r'<br/><font color="blue">cP: ' + str(x6Matrix_element['closedPart']) + r'</font>'
                else:
                    level_closedPart =  r'<br/>cP: ' + str(x6Matrix_element['closedPart'])
                # if id(x6Matrix_element['reinvestCount']) in new_items_id_set:
                #     level_reinvestCount =  r'<br/><font color="blue">b: ' + str(x6Matrix_element['reinvestCount']) + r'</font>'
                # else:
                #     level_reinvestCount =  r'<br/>b: ' + str(x6Matrix_element['reinvestCount'])

                level_xlabel = r'<' + level_referrer + level_blocked + level_closedPart + r'>'
                if id(x6Matrix_element['currentReferrer']) in new_items_id_set and id(x6Matrix_element['blocked']) in new_items_id_set and id(x6Matrix_element['closedPart']) in new_items_id_set:
                    level_node = dot_x6.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box',
                                         color='blue')
                elif str(x6Matrix_element['blocked']) == 'True':
                    level_node = dot_x6.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box',
                                         color='red')
                else:
                    level_node = dot_x6.node(level_node_name,
                                         #level_node_name + r'\n' + level_xlabel,
                                         level_xlabel,
                                         shape='box')
                first_referrals = x6Matrix_element['firstLevelReferrals']
                second_referrals = x6Matrix_element['secondLevelReferrals']
                for index_2 in range(0, len(first_referrals)):
                # referral in first_referrals:
                    referral = first_referrals[index_2].get()
                    referral_label = construct_concise_label(all_user_dict[referral], new_items_id_set)
                    referral_graph_name = level_node_name + '_l1_' + referral + str(index_2)
                    if id(all_user_dict[referral]['name']) in new_items_id_set and id(all_user_dict[referral]['id']) in new_items_id_set:
                        dot_x6.node(referral_graph_name, referral_label, color="blue")
                    else:
                        dot_x6.node(referral_graph_name, referral_label)
                    dot_x6.edge(level_node_name, referral_graph_name)
                if len(second_referrals) > 0:
                    second_tree_parent_name = level_node_name + '_l2point'
                    second_tree_parent_point = dot_x6.node(second_tree_parent_name, '', shape='point')
                    #second_tree_parent_point = dot_x6.node(second_tree_parent_name, 'x', shape='plain')
                    dot_x6.edge(level_node_name, second_tree_parent_name)
                    for index_3 in range(0, len(second_referrals)):
                        referral = second_referrals[index_3].get()
                        referral_label = construct_concise_label(all_user_dict[referral], new_items_id_set)
                        referral_graph_name = level_node_name + '_l2_' + referral + str(index_3)
                        if id(all_user_dict[referral]['name']) in new_items_id_set and id(all_user_dict[referral]['id']) in new_items_id_set:
                            dot_x6.node(referral_graph_name, referral_label, color="blue")
                        else:
                            dot_x6.node(referral_graph_name, referral_label)
                        dot_x6.edge(second_tree_parent_name, referral_graph_name)
        else:
            if id(user['name']) in new_items_id_set and id(user['id']) in new_items_id_set:
                level_node = dot_x6.node(level_node_name, '', shape='point', color="blue")
                #level_node = dot_x6.node(level_node_name,  r'<' +'<font color="blue">x</font>' + r'>', shape='plain', color="blue")
            else:
                level_node = dot_x6.node(level_node_name, '', shape='point')
                #level_node = dot_x6.node(level_node_name, r'<' +'<font color="red">x</font>' + r'>', shape='plain')
        dot_x6.edge('user' + title_x6, level_node_name)
    return (dot_x3, dot_x6)


def graph_user_state(filename: str, user: User, all_user_dict: Dict[str, User]):
    dot_x3, dot_x6 = generate_graph_user_state(user, all_user_dict, False, set())
    dot_x3.render(filename + '_x3')
    dot_x6.render(filename + '_x6')

def graph_full_state(filename: str, graph_title: str, all_user_dict: Dict[str, User], all_user_list_queryorder: List[str]):
    total_state_graph = Graph(format='pdf')
    total_state_graph.attr(label=graph_title, labelloc = 't')#, ratio='1')
    for name in all_user_list_queryorder:
        if name in all_user_dict:
            curr_dot_x3, curr_dot_x6 = generate_graph_user_state(all_user_dict[name], all_user_dict, True, set())
            total_state_graph.subgraph(curr_dot_x3)
            total_state_graph.subgraph(curr_dot_x6)
    total_state_graph.render(filename)

def graph_full_state_per_user(filename: str, all_user_dict: Dict[str, User], all_user_list_queryorder: List[str], new_items_id_set: Set[int]):
    for name in all_user_list_queryorder:
        if name in all_user_dict:
            total_state_graph = Graph(format='pdf')
            curr_dot_x3, curr_dot_x6 = generate_graph_user_state(all_user_dict[name], all_user_dict, True, new_items_id_set)
            total_state_graph.subgraph(curr_dot_x3)
            total_state_graph.subgraph(curr_dot_x6)
            total_state_graph.render(filename + '_' + str(name))




# testing code before integrating with expiriment.py
if __name__ == '__main__':
    print('Running Test')
    u_alpha = User({
        'name':
            MutableString('alpha'),
        'id':
            MutableInt(1),
        'referrer':
            MutableString('0x0'),
        'partnersCount':
            MutableInt(1),
        'balanceDelta':
            MutableInt(171060000000000000),
        'balanceLastChange':
            0,
        'activeX3Levels': [
            True, True, True, True, True, True, True, True, True, True, True, True
        ],
        'activeX6Levels': [
            True, True, True, True, True, True, True, True, True, True, True, True
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': [MutableString('bravo'), MutableString('bravo')]
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': [MutableString('bravo')]
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [MutableString('bravo')],
            'secondLevelReferrals': [MutableString('charlie'), MutableString('delta')]
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, {
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('0x0'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }]
    })

    u_bravo = User({
        'name':
            MutableString('bravo'),
        'id':
            MutableInt(2),
        'referrer':
            MutableString('alpha'),
        'partnersCount':
            MutableInt(5),
        'balanceDelta':
            MutableInt(74547200000000000),
        'balanceLastChange':
            74047200000000000,
        'activeX3Levels': [
            True, True, False, False, False, False, False, False, False, False,
            False, False
        ],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('alpha'),
            # 'reinvestCount': MutableInt(0),
            'referrals': [MutableString('foxtrot'), MutableString('golf')]
        }, {
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('alpha'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('alpha'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [MutableString('charlie'), MutableString('delta')],
            'secondLevelReferrals': [MutableString('echo'), MutableString('foxtrot'), MutableString('golf')]
        }, None, None, None, None, None, None, None, None, None, None, None]
    })
    u_charlie = User({
        'name':
            MutableString('charlie'),
        'balanceDelta':
            MutableInt(-50378700000000000),
        'balanceLastChange':
            0,
        'referrer':
            MutableString('bravo'),
        'id':
            MutableInt(3),
        'partnersCount':
            MutableInt(0),
        'activeX3Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('bravo'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None, None],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('bravo'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [MutableString('echo'), MutableString('golf')],
            'secondLevelReferrals': []
        }, None, None, None, None, None, None, None, None, None, None, None]
    })
    u_delta = User({
        'name':
            MutableString('delta'),
        'balanceDelta':
            MutableInt(-50318700000000000),
        'balanceLastChange':
            0,
        'referrer':
            MutableString('bravo'),
        'id':
            MutableInt(4),
        'partnersCount':
            MutableInt(0),
        'activeX3Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('bravo'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None, None],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('bravo'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [MutableString('foxtrot')],
            'secondLevelReferrals': []
        }, None, None, None, None, None, None, None, None, None, None, None]
    })
    u_echo = User({
        'name':
            MutableString('echo'),
        'balanceDelta':
            MutableInt(-50369400000000000),
        'balanceLastChange':
            0,
        'referrer':
            MutableString('bravo'),
        'id':
            MutableInt(5),
        'partnersCount':
            MutableInt(0),
        'activeX3Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('bravo'),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None, None],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('charlie'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, None, None, None, None, None, None, None, None, None, None, None]
    })
    u_foxtrot = User({
        'name':
            MutableString('foxtrot'),
        'balanceDelta':
            MutableInt(-50354400000000000),
        'balanceLastChange':
            0,
        'referrer':
            MutableString('bravo'),
        'id':
            MutableInt(6),
        'partnersCount':
            MutableInt(0),
        'activeX3Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('bravo'),
            # 'reinvestCount': MutableInt(0),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None, None],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('delta'),
            # 'reinvestCount': MutableInt(0),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, None, None, None, None, None, None, None, None, None, None, None]
    })

    u_golf = User({
        'name':
            MutableString('golf'),
        'balanceDelta':
            MutableInt(-50324400000000000),
        'balanceLastChange':
            -2500000000000,
        'referrer':
            MutableString('bravo'),
        'id':
            MutableInt(7),
        'partnersCount':
            MutableInt(0),
        'activeX3Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'activeX6Levels': [
            True, False, False, False, False, False, False, False, False,
            False, False, False
        ],
        'x3Matrix': [{
            'blocked': MutableBool(False),
            'currentReferrer': MutableString('bravo'),
            'referrals': []
        }, None, None, None, None, None, None, None, None, None, None, None],
        'x6Matrix': [{
            'blocked': MutableBool(False),
            'closedPart': MutableString('0x0'),
            'currentReferrer': MutableString('charlie'),
            'firstLevelReferrals': [],
            'secondLevelReferrals': []
        }, None, None, None, None, None, None, None, None, None, None, None]
    })

    all_user_dict = {
        'alpha': u_alpha,
        'bravo': u_bravo,
        'charlie': u_charlie,
        'delta': u_delta,
        'echo': u_echo,
        'foxtrot': u_foxtrot,
        'golf': u_golf
    }
    all_user_list = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf']

    #graph_user_state('graphtest_bravo', u_bravo, all_user_dict)
    #graph_full_state('graphtest_state', 'State Test', all_user_dict, all_user_list)
    if u_alpha:
        if u_alpha['x3Matrix']:
            if u_alpha['x3Matrix'][0]:
                test_delta_coloring = {id(u_alpha['name']), id(u_alpha['partnersCount']), id(u_alpha['x3Matrix'][0]['blocked']),id(u_alpha['x3Matrix'][0]['currentReferrer'])} # type: ignore
    graph_full_state_per_user('graphtest_state', all_user_dict, all_user_list, test_delta_coloring)
