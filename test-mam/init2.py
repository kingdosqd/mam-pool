#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
import time

#sha256address=187ssr7erv8dq1eb1gb4mqxe30s89mb8bmmvr0jgj4e3x1sy4kzm27jpv
#sha256key=28efbfda61b473c37549d02784648d89fe21ff082b7a42da9ef97b0b83cdb1a9


#    "privkey" : "24d0ad81e6af0adc350b0f5962596d409a320a96cd7b6c2ce5dad2e65568a39a",
#    "pubkey" : "e89fc4e7d08723124a8037a50b2d9a5006c3f54bc98261b9701bdad81d9cf341"
#    "addr" : 187ssr7erv8dq1eb1gb4mqxe30s89mb8bmmvr0jgj4e3x1sy4kzm27jpv

def run_cmd(cmd):
    print(cmd)
    #info = subprocess.getoutput(cmd)
    #print(info)
    
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    print(info.stdout)
    time.sleep(1)

run_cmd('minemon-cli stop')
run_cmd('rm -rf ~/.minemon/*')
run_cmd('cp ./minemon2.conf ~/.minemon/minemon.conf')
#subprocess.run(['minemon', '-daemon'])
subprocess.run('minemon -daemon -debug',shell=True)
time.sleep(2)
run_cmd('minemon-cli importprivkey 24d0ad81e6af0adc350b0f5962596d409a320a96cd7b6c2ce5dad2e65568a39a 123')
run_cmd('minemon-cli unlockkey e89fc4e7d08723124a8037a50b2d9a5006c3f54bc98261b9701bdad81d9cf341 123 0')

# 添加挖矿模板
cmd = "minemon-cli addnewtemplate mint '{\"mint\": \"883f29fb7740f8e625159cb6bcee42cf3ac460be8b9fcb839ccbfeda3744b217\", \"spent\": \"187ssr7erv8dq1eb1gb4mqxe30s89mb8bmmvr0jgj4e3x1sy4kzm27jpv\"}'"
run_cmd(cmd)
# 20g06drhext3xna72y20kyzjvxgfh8qg0chkxk4t6sk4n0hc97ncest2n

# 添加投票模板
cmd = "minemon-cli addnewtemplate mintpledge '{\"owner\": \"187ssr7erv8dq1eb1gb4mqxe30s89mb8bmmvr0jgj4e3x1sy4kzm27jpv\", \"powmint\": \"20g06drhext3xna72y20kyzjvxgfh8qg0chkxk4t6sk4n0hc97ncest2n\", \"rewardmode\":1}'"

run_cmd(cmd)
# 21c01yx9yh6j3d43hexpak69pwpdnvr8jekhm08nzc22xktyyka9nqdve

# 赎回模板，投票模板只能向赎回模板转账
cmd = "minemon-cli addnewtemplate mintredeem '{\"owner\": \"187ssr7erv8dq1eb1gb4mqxe30s89mb8bmmvr0jgj4e3x1sy4kzm27jpv\", \"nonce\": 1}'"
run_cmd(cmd)
# 21g0152mtw1vmwn4n9s2nfgm672yvw9656nq2njydpspnc8652d20f4d5

while True:
    time.sleep(3)
    json_str = subprocess.getoutput('minemon-cli getbalance')
    objs = json.loads(json_str)
    is_break = False
    for obj in objs:
        if obj["address"] == "20g06drhext3xna72y20kyzjvxgfh8qg0chkxk4t6sk4n0hc97ncest2n" and obj["avail"]  > 200:
            is_break = True
            break

    # 给挖矿地址投票
    if is_break:
        cmd = "minemon-cli sendfrom 20g06drhext3xna72y20kyzjvxgfh8qg0chkxk4t6sk4n0hc97ncest2n 21c01yx9yh6j3d43hexpak69pwpdnvr8jekhm08nzc22xktyyka9nqdve 200"
        run_cmd(cmd)
        break
    run_cmd("minemon-cli getforkheight")
            
while True:
    run_cmd('minemon-cli getbalance')
    run_cmd("minemon-cli getforkheight")