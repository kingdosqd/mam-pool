#!/bin/bash
minemon-cli stop
rm -rf ~/.minemon/*
cp ./minemon.conf ~/.minemon/
minemon -daemon
sleep 1
minemon-cli importprivkey 42b889a2668eda6d78682c23b5651fb76b5aac2b71caba1aa23b6b14d5ce75b7 123
minemon-cli unlockkey 57e7d8bb1119ec37d76f0785e73b1a3fa288a5aa1e84925fe47a5d73b68dba91 123 0

# 添加挖矿模板
minemon-cli addnewtemplate mint '{"mint": "883f29fb7740f8e625159cb6bcee42cf3ac460be8b9fcb839ccbfeda3744b217", "spent": "1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda"}'
# 20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf

# 添加投票模板
minemon-cli addnewtemplate mintpledge '{"owner": "1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda", "powmint": "20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf", "rewardmode":1}'
# 21c0ccarf3kpr87r2peet1p1ngsmsze8qdsmza6kmws9fz6k0v9y7fmnc

# 赎回模板，投票模板只能向赎回模板转账
minemon-cli addnewtemplate mintredeem '{"owner": "1j6x8vdkkbnxe8qwjggfan9c8m8zhmez7gm3pznsqxgch3eyrwxby8eda", "nonce": 1}'
# 21g02epzpp8txzbtg44t6stf78djkwt2cz5w61mvsy1t00ddywwks3b68

# 给挖矿地址投票
#minemon-cli sendfrom 20g053vhn4ygv9m8pzhevnjvtgbbqhgs66qv31ez39v9xbxvk0ynqmeyf 21c0ccarf3kpr87r2peet1p1ngsmsze8qdsmza6kmws9fz6k0v9y7fmnc 100
