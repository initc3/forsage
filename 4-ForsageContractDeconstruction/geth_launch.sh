#!/usr/bin/env bash

rm -rf forsagetestdata
mkdir forsagetestdata
geth init --datadir forsagetestdata ./forsage_test_genesis.json
printf "\n\n"
geth --nodiscover --maxpeers 0 --ipcpath ./forsage_geth.ipc --datadir ./forsagetestdata --port "31313" --identity "forsagetester" --miner.gaslimit 10000000 #--mine --miner.threads 1 --miner.etherbase "0x673985274a0FD8A8d7d21CE2102447DaD72a2def" # --verbosity 5
#geth --nodiscover --maxpeers 0 --ipcpath ./forsage_geth.ipc --datadir ./forsagetestdata --port "31313" --identity "forsagetester" --miner.gaslimit 10000000 --http --http.api 'personal,eth,net,web3,admin' --http.addr '0.0.0.0' --http.vhosts '*' --rpccorsdomain '*' --allow-insecure-unlock
