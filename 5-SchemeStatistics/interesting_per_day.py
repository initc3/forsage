#!/usr/bin/env python3

__author__='tyler'

import csv
from typing import Dict
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

months = mdates.MonthLocator()  # every month

outer_name_dict: Dict[str, Dict[str, int]] = {}
global_counter = 0


every_day = ['04/01/2020', '04/02/2020', '04/03/2020', '04/04/2020', '04/05/2020', '04/06/2020', '04/07/2020', '04/08/2020', '04/09/2020', '04/10/2020', '04/11/2020', '04/12/2020', '04/13/2020', '04/14/2020', '04/15/2020', '04/16/2020', '04/17/2020', '04/18/2020', '04/19/2020', '04/20/2020', '04/21/2020', '04/22/2020', '04/23/2020', '04/24/2020', '04/25/2020', '04/26/2020', '04/27/2020', '04/28/2020', '04/29/2020', '04/30/2020', '05/01/2020', '05/02/2020', '05/03/2020', '05/04/2020', '05/05/2020', '05/06/2020', '05/07/2020', '05/08/2020', '05/09/2020', '05/10/2020', '05/11/2020', '05/12/2020', '05/13/2020', '05/14/2020', '05/15/2020', '05/16/2020', '05/17/2020', '05/18/2020', '05/19/2020', '05/20/2020', '05/21/2020', '05/22/2020', '05/23/2020', '05/24/2020', '05/25/2020', '05/26/2020', '05/27/2020', '05/28/2020', '05/29/2020', '05/30/2020', '05/31/2020', '06/01/2020', '06/02/2020', '06/03/2020', '06/04/2020', '06/05/2020', '06/06/2020', '06/07/2020', '06/08/2020', '06/09/2020', '06/10/2020', '06/11/2020', '06/12/2020', '06/13/2020', '06/14/2020', '06/15/2020', '06/16/2020', '06/17/2020', '06/18/2020', '06/19/2020', '06/20/2020', '06/21/2020', '06/22/2020', '06/23/2020', '06/24/2020', '06/25/2020', '06/26/2020', '06/27/2020', '06/28/2020', '06/29/2020', '06/30/2020', '07/01/2020', '07/02/2020', '07/03/2020', '07/04/2020', '07/05/2020', '07/06/2020', '07/07/2020', '07/08/2020', '07/09/2020', '07/10/2020', '07/11/2020', '07/12/2020', '07/13/2020', '07/14/2020', '07/15/2020', '07/16/2020', '07/17/2020', '07/18/2020', '07/19/2020', '07/20/2020', '07/21/2020', '07/22/2020', '07/23/2020', '07/24/2020', '07/25/2020', '07/26/2020', '07/27/2020', '07/28/2020', '07/29/2020', '07/30/2020', '07/31/2020', '08/01/2020', '08/02/2020', '08/03/2020', '08/04/2020', '08/05/2020', '08/06/2020', '08/07/2020', '08/08/2020', '08/09/2020', '08/10/2020', '08/11/2020', '08/12/2020', '08/13/2020', '08/14/2020', '08/15/2020', '08/16/2020', '08/17/2020', '08/18/2020', '08/19/2020', '08/20/2020', '08/21/2020', '08/22/2020', '08/23/2020', '08/24/2020', '08/25/2020', '08/26/2020', '08/27/2020', '08/28/2020', '08/29/2020', '08/30/2020', '08/31/2020', '09/01/2020', '09/02/2020', '09/03/2020', '09/04/2020', '09/05/2020', '09/06/2020', '09/07/2020', '09/08/2020', '09/09/2020', '09/10/2020', '09/11/2020', '09/12/2020', '09/13/2020', '09/14/2020', '09/15/2020', '09/16/2020', '09/17/2020', '09/18/2020', '09/19/2020', '09/20/2020', '09/21/2020', '09/22/2020', '09/23/2020', '09/24/2020', '09/25/2020', '09/26/2020', '09/27/2020', '09/28/2020', '09/29/2020', '09/30/2020']

every_day_datetime = []
for day in every_day:
    every_day_datetime.append(datetime.datetime.strptime(day, '%m/%d/%Y'))


if __name__=='__main__':
    list_files = [
            'Tether.csv',
            'usdc.csv',
            'Uniswap.csv',
            'Easy_Club.csv',
            'MMMBSC_Global.csv',
            #'WorldUnitedCoins.csv',
            #'Paxos.csv',
            #'Unitoken.csv',
            'Forsage.csv'
            ]
    color_dict = {'usdc': 'darkslategray', 'Uniswap': 'darkslateblue', 'Forsage': 'red', 'Easy_Club': 'darkgoldenrod', 'MMMBSC_Global': 'goldenrod', 'Tether':'teal'}
    label_dict = {'usdc': 'USDC', 'Uniswap': 'Uniswap V2', 'Forsage': 'Forsage', 'Easy_Club': 'Easy Club', 'MMMBSC_Global': 'MMBSC Global', 'Tether':'Tether'}
    fig, ax = plt.subplots()
    for input_file_name in list_files:
        contract_name = input_file_name.split(".")[0]
        with open(input_file_name, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for line in csv_reader:
                #headers = ["hash","block_number","from_address","to_address","value","gas_price","gas_used","txfee","block_timestamp","status"]
                block_timestamp_dt = datetime.datetime.utcfromtimestamp(int(line[8]))
                string_day = block_timestamp_dt.strftime("%m/%d/%Y")
                inner_count_dict = outer_name_dict.get(contract_name, {})
                count_this_day = inner_count_dict.get(string_day, 0)
                count_this_day += 1
                inner_count_dict[string_day] = count_this_day
                outer_name_dict[contract_name] = inner_count_dict
                global_counter += 1
                if global_counter % 100000 == 0:
                    print('Processed {} {}'.format(input_file_name, global_counter))


        counts_list = []
        inner_count_dict = outer_name_dict.get(contract_name, {})
        for day in every_day:
            count_this_day = inner_count_dict.get(day, 0)
            counts_list.append(count_this_day)

        assert(len(every_day) == len(counts_list))

        if contract_name == "Forsage":
            ax.plot(every_day_datetime, counts_list, label=label_dict[contract_name], color=color_dict[contract_name], linewidth=1.5)
        else:
            ax.plot(every_day_datetime, counts_list, label=label_dict[contract_name], color=color_dict[contract_name])
    ax.xaxis.set_major_locator(months)
    ax.set_xlim(every_day_datetime[0], every_day_datetime[-1])
    date_xaxis_formatter = mdates.DateFormatter('%b %y')
    ax.xaxis.set_major_formatter(date_xaxis_formatter)
    ax.legend()
    #plt.yscale('log')
    ax.set_xlabel("Date")
    ax.set_ylabel("Num TX Per Day")
    ax.set_yticks([50000, 100000, 150000, 200000, 250000, 300000])
    ax.set_yticklabels(["50K", "100K", "150K", "200K", "250K", "300K"])
    fig.savefig("popular_contracts.pdf", bbox_inches="tight")


# print(outer_name_dict)
# print(every_day)
# print(counts_list)
# #print(outer_name_dict['usdc'])
