#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import json
import time
import pymysql
import bbc_lib


connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="root", db="minemon")

def ExecSql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e,sql)
        return 0

def get_block_data(height):
    cmd = 'minemon-cli getblockhash %d' % height
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    if info.stdout == "":
        print("exit at height :",height)
    objs = json.loads(info.stdout)
    cmd = 'minemon-cli getblock %s' % objs[0]
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    objs = json.loads(info.stdout)
    sql = "insert into block(height,bits,time)values(%s,'%s',%s)" % (objs["height"],objs["bits"],objs["time"])
    ExecSql(sql)

def Run():
    cmd = 'minemon-cli getforkheight'
    info = subprocess.run(cmd, shell=True,stdout=subprocess.PIPE,universal_newlines=True)
    height = int(info.stdout)
    for h in range(1,height+1):
        print(h)
        get_block_data(h)

def Show():
    cursor = connection.cursor()
    cursor.execute("select * from block")
    results = cursor.fetchall()
    bits = ""
    time_begin = 0
    for row in results:
        if row[1] % 30 == 0 or row[1] == 1:
            # begin
            bits = row[2]
            time_begin = row[3]
        if row[1] % 30 == 29:
            print(row[1],bits ,(row[3] - time_begin) / 30)
if __name__ == '__main__':
    #ExecSql("delete from block;")
    #Run()
    Show()
    #print((30 + 30) % 30)
    #print((59 + 30) % 30)