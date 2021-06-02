#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
import time
import pymysql
import traceback 
import sys
import os

def GetTime(height):
    cmd = "bitcoin-cli -testnet getblockhash %d" % height
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    cmd = "bitcoin-cli -testnet getblock %s" % info.stdout.strip("\n")
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    b = json.loads(info.stdout)
    return b["time"]

if __name__ == '__main__':
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", db="minemon")
        while True:
            cur = conn.cursor()
            sql = "SELECT id,block_height FROM rewarddetails where block_time is null;"
            cur.execute(sql)
            bs = cur.fetchall()
            for b in bs:
                sql = "update rewarddetails set block_time = %d where id = %d " % (GetTime(b[1]),b[0])
                cur.execute(sql)
            conn.commit()
            time.sleep(3)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"time.sleep(3)")
    except KeyboardInterrupt:
        sys.exit()
    except:
        time.sleep(3)
        traceback.print_exc()
        print("restart.....")
        python = sys.executable
        os.execl(python, python, *sys.argv)