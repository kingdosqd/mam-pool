#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
import time
import pymysql


connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", db="minemon")

def ExecSql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        return 0


def get_tx_data(txid,height):
    cmd = 'minemon-cli gettransaction %s' % txid
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    objs = json.loads(info.stdout)
    tx = objs["transaction"]
    sql = "insert tx(txid,height,type,sendfrom,sendto,amount,txfee)values('%s',%d,'%s','%s','%s',%f,%f)" % (tx["txid"],height,tx["type"],tx["sendfrom"],tx["sendto"],tx["amount"],tx["txfee"])
    #print(sql)
    ExecSql(sql)

def get_block_data(height):
    cmd = 'minemon-cli getblockhash %d' % height
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    if info.stdout == "":
        print("exit at height :",height)
    objs = json.loads(info.stdout)
    cmd = 'minemon-cli getblock %s' % objs[0]
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    objs = json.loads(info.stdout)
    get_tx_data(objs["txmint"],height)
    for txid in objs["tx"]:
        get_tx_data(txid,height)

if __name__ == '__main__':
    cmd = 'minemon-cli getforkheight'
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    height = int(info.stdout)
    for h in range(1,height):
        #print(h)
        get_block_data(h)
