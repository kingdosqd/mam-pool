#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
import time

def Vote(pledgefee):
    cmd = "minemon-cli makekeypair"
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    obj = json.loads(info.stdout)
    cmd = "minemon-cli getpubkeyaddress " + obj["pubkey"]
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    obj["spent"] = info.stdout.strip("\n")
    obj["pledgefee"] = pledgefee
    cmd = "minemon-cli addnewtemplate mint '{\"pledgefee\": %d, \"spent\": \"%s\"}'" % (pledgefee * 1000,obj["spent"])
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    obj["pow_addr"] = info.stdout.strip("\n")
    return obj

data = {}
for i in range(100):
   data[i] = Vote(0.95)

file_data = json.dumps(data,indent=4,ensure_ascii=False)
with open('./privkey.json','w') as f:
    f.write(file_data)

for key in data:
    del data[key]["privkey"]

file_data = json.dumps(data,indent=4,ensure_ascii=False)
with open('./pubkey.json','w') as f:
    f.write(file_data)
