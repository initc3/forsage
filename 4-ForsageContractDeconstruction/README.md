# Forsage Smart Contract Deconstruction

This is the code for section 4 in the paper, where we analyze the smart contract's code.


## Simulator related files

```
* forsage_compiled.json - compiled form of the Forsage solidity code for the smart contract
* forsage_abi.json - ABI for the solidity smart contract
* forsage_abi.py - same Forsage ABI but more easily accessible in python
* forsage_test_genesis.json - test genesis state for Geth so you have a set of user accounts with money to work with for the simulator
* test_addresses.csv - list of test addresses
* geth_launch.sh - launches Geth with the right parameters to run a localhost private node for the simulator
* graphing.py - Openviz graphing module to make pictures of the pyramid data structures of the Forsage smart contract. Also used for Figure 1 in the paper
* expiriment_constants.py - random constant values keep clutter out of expiriment.py
* expiriment.py - the core simulator code. Order of transactions submitted in the main method will determine the state of the simulation. Simulation visualizations are then put in the statepng folders, one pdf for each user's state for every transaction step in the simulation
```

## Data collection

```
* ethereum_etl_runner.py - harvests transaction raw data (who sent how much and function calls made) out of a Geth node and puts it into a CSV
* calculate_tx_fee_info.py - puts data together from etl_runner.py into a more convienent combined csv
```

## Graph generation

```
* percent_registration_vs_buynewlevel.py - simple counts of which transactions called which function
* collect_referrers.py - for every account that is in the global Forsage state, find out how many referrers they have set 
* make_buy_new_level_histogram.py - generates Figure 4 in the paper
* make_referrer_counts_histogram.py - generates Figure 5 in the paper
* make_sstore_stats.py - generates the data shown in Table 1 in the paper
* make_txcost_histogram.py - generates Figure 2 in the paper
```
