#!/usr/bin/env python
# -*- coding: utf-8 -*-

#sha256address=1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda
#sha256key=28efbfda61b473c37549d02784648d89fe21ff082b7a42da9ef97b0b83cdb1a9

import subprocess
import json
import time

def run_cmd(cmd):
    print(cmd)
    #info = subprocess.getoutput(cmd)
    #print(info)
    
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    print(info.stdout)
    time.sleep(1)

run_cmd('minemon-cli stop')
run_cmd('rm -rf ~/.minemon/*')
run_cmd('cp ./minemon.conf ~/.minemon/')
#subprocess.run(['minemon', '-daemon'])
subprocess.run('minemon -daemon',shell=True)
time.sleep(2)
run_cmd('minemon-cli importprivkey 42b889a2668eda6d78682c23b5651fb76b5aac2b71caba1aa23b6b14d5ce75b7 123')
run_cmd('minemon-cli unlockkey 57e7d8bb1119ec37d76f0785e73b1a3fa288a5aa1e84925fe47a5d73b68dba91 123 0')

# 添加挖矿模板
cmd = "minemon-cli addnewtemplate mint '{\"mint\": \"883f29fb7740f8e625159cb6bcee42cf3ac460be8b9fcb839ccbfeda3744b217\", \"spent\": \"1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda\"}'"
run_cmd(cmd)
# 20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf

# 添加投票模板
cmd = "minemon-cli addnewtemplate mintpledge '{\"owner\": \"1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda\", \"powmint\": \"20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf\", \"rewardmode\":1}'"
run_cmd(cmd)
# 21c0ccarf3kpr87r2peet1p1ngsmsze8qdsmza6kmws9fz6k0v9y7fmnc

# 赎回模板，投票模板只能向赎回模板转账
cmd = "minemon-cli addnewtemplate mintredeem '{\"owner\": \"1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda\", \"nonce\": 1}'"
run_cmd(cmd)
# 21g02epzpp8txzbtg44t6stf78djkwt2cz5w61mvsy1t00ddywwks3b68


#    "privkey" : "1dc744f645627179af2d938d6d3294fdd447bb96caf861c1db05cd874adffcea",
#    "pubkey" : "6430b5ac60d61914121bd8db1d00fa10422d0a935f1d3ef9a941f9936e5d7979"
#    "addr" : "1f5wntvmkz50tky9y3nfs62hd888fm00xvfc1p4gm37b61b5n61j54tet"
cmd = "minemon-cli addnewtemplate mintpledge '{\"owner\": \"1f5wntvmkz50tky9y3nfs62hd888fm00xvfc1p4gm37b61b5n61j54tet\", \"powmint\": \"20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf\", \"rewardmode\":1}'"
run_cmd(cmd)
# 21c06w107f5rr6wj3ezeh8w0bn40pnkrdp7nnvb87py784m6efsgzwxpr

while True:
    time.sleep(3)
    json_str = subprocess.getoutput('minemon-cli getbalance')
    objs = json.loads(json_str)
    is_break = False
    for obj in objs:
        if obj["address"] == "20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf" and obj["avail"]  > 250:
            is_break = True
            break

    # 给挖矿地址投票
    if is_break:
        cmd = "minemon-cli sendfrom 20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf 21c0ccarf3kpr87r2peet1p1ngsmsze8qdsmza6kmws9fz6k0v9y7fmnc 100"
        run_cmd(cmd)
        cmd = "minemon-cli sendfrom 20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf 21c06w107f5rr6wj3ezeh8w0bn40pnkrdp7nnvb87py784m6efsgzwxpr 150"
        run_cmd(cmd)
        break
    run_cmd("minemon-cli getforkheight")
            
while True:
    run_cmd('minemon-cli getbalance')
    run_cmd("minemon-cli getforkheight")