#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 3.6.9
# sqlalchemy 1.4.15(sqlalchemy.__version__)
'''
检查项:
1:pow奖励金额的正确性
2:检查发放奖励，投票金额，资金池金额
'''

import decimal
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR,DECIMAL
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal,getcontext

from sqlalchemy.sql.expression import null, true
from operator import add, itemgetter, attrgetter

context = decimal.getcontext()
context.rounding = decimal.ROUND_DOWN

Base = declarative_base()

engine = create_engine("mysql+pymysql://root:root@localhost:3306/minemon", encoding="utf-8")

class Tx(Base):
    __tablename__ = 'tx'
    id = Column(INTEGER, primary_key=True)
    txid = Column(VARCHAR(256), nullable=False)
    height = Column(INTEGER)
    type = Column(VARCHAR(256), nullable=False)
    sendfrom = Column(VARCHAR(256), nullable=False)
    sendto = Column(VARCHAR(256), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    txfee = Column(DECIMAL, nullable=False)
    pool_in = Column(VARCHAR(256), nullable=False)
    miner_in = Column(VARCHAR(256), nullable=False)

def TestWork():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).all()
    info = {}
    for tx in Txs:
        if tx.type == 'work':
           info[tx.height] = {
               "work": tx.amount, 
               "txfee" : []}
        else:
            info[tx.height]["txfee"].append(tx.txfee)
    for key in info:
        assert info[key]["work"] == sum(info[key]["txfee"]) + + Decimal("38.2"),"pow amount err"
    print("TestWork OK")

def SetVote(Vote,tx):
    if tx.pool_in in Vote:
        Vote[tx.pool_in]["v"] += tx.amount
        if tx.sendto in Vote[tx.pool_in]["info"]:
            Vote[tx.pool_in]["info"][tx.sendto]["vote"] += tx.amount
        else:
            Vote[tx.pool_in]["info"][tx.sendto] = {
                "vote":tx.amount,
                "stake":0,
                "stake_":0
            }
    else:
        Vote[tx.pool_in] = {
            "v":tx.amount,
            "info":{
                tx.sendto : {
                    "vote":tx.amount,
                    "stake":0,
                    "stake_":0
                }
            }
        }

def SetVoteStake(Vote,pool_in,stake,height):
    if pool_in not in Vote:
        return
    vote_sum = Decimal("0")
    for miner in Vote[pool_in]["info"]:
        vote_sum += Vote[pool_in]["info"][miner]["vote"]

    for miner in Vote[pool_in]["info"]:
        v = Vote[pool_in]["info"][miner]["vote"]
        Vote[pool_in]["info"][miner]["stake"] += stake * v / vote_sum
        Vote[pool_in]["info"][miner]["stake_"] = stake * v / vote_sum

def DelVoteStake(Vote,pool_addr):
    for pool_in in Vote:
        for miner in Vote[pool_in]["info"]:
            Vote[pool_in]["info"][miner]["stake"] = Vote[pool_in]["info"][miner]["stake_"]
            Vote[pool_in]["info"][miner]["stake_"] = 0
    
    for pool_in in Vote:
        if pool_in != pool_addr:
            for miner in Vote[pool_in]["info"]:
                Vote[pool_in]["info"][miner]["stake"] = Decimal("0")
                Vote[pool_in]["info"][miner]["stake_"] = Decimal("0")
    

def CheckVoteStake(Vote,tx,pool_addr):
    stake = tx.amount
    for pool_in in Vote:
        for miner in Vote[pool_in]["info"]:
            if miner == tx.sendto:
                a = Vote[pool_in]["info"][miner]["stake"]
                b = Decimal("0")
                if tx.pool_in == pool_addr:
                    b = Vote[pool_in]["info"][miner]["stake_"]
                #context.rounding = decimal.ROUND_HALF_UP
                c = round(a - b,6)
                stake = round(stake,6)
                assert stake == c,"err"
                #if abs(stake - c) > Decimal("0.000050"):
                #    print("err",stake ,c)
                #    exit()
                #print(abs(round(stake - c,6)))
    

def TestAmount():
    BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT = 5
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).all()
    info = {}
    Vote = {}
    for tx in Txs:
        if tx.height not in info:
            info[tx.height] = {
                "work":None,
                "stake":[],
                "vote":[]}
        if tx.type == 'work':
            info[tx.height]["work"] = tx
        if tx.type == 'stake':
            info[tx.height]["stake"].append(tx)
        if tx.type == 'token' and tx.sendto[0:4] == "21c0":
            info[tx.height]["vote"].append(tx)

    N_ = Decimal("100")
    M_ = N_ * 100
    TotalReward = Decimal("0")
    MoneySupply = Decimal("0")
    Stakes = []
    for height in info:
        TotalReward = TotalReward + Decimal("100.0")
        MoneySupply = MoneySupply + Decimal("38.2")
        Stake = Decimal("0")
        if info[height]["work"].sendto in Vote:
            if Vote[info[height]["work"].sendto]["v"] > M_:
                Stake = round((TotalReward - MoneySupply),6)
            else:
                Stake = round((TotalReward - MoneySupply) * Vote[info[height]["work"].sendto]["v"] / M_,6)
        # 让抵押者分掉收益
        SetVoteStake(Vote,info[height]["work"].sendto,Stake,height)
        #print(height,Stake)
        Stakes.append(Stake)
        MoneySupply += Stake
        
        if height % BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT == 1:
            sum_ = Decimal("0")
            for tx in info[height]["stake"]:
                sum_ += tx.amount
                #更新投票
                SetVote(Vote,tx)
                #检查发放是否正确
                CheckVoteStake(Vote,tx,info[height]["work"].sendto)
            sum2_ = sum(Stakes[:-1])
            assert sum_ == sum2_,"奖励发放总金额错误"
            Stakes = Stakes[-1:]
            DelVoteStake(Vote,info[height]["work"].sendto)
        for tx in info[height]["vote"]:
            #更新投票
            SetVote(Vote,tx)

    session.close()
    print("TestAmount OK")

if __name__ == '__main__':
    context.rounding = decimal.ROUND_HALF_UP
    # 11 20.394000
    # 12 21.636180
    # 13 22.841094
    # 14 24.009861
    # 15 25.143565

    # 76.0164670000
    # 38.0082330000
    d16_1 = Decimal("76.0164670000")
    d16_2 = Decimal("38.0082330000")

    d11 = Decimal("20.394000")
    d12 = Decimal("21.636180")
    d13 = Decimal("22.841094")
    d14 = Decimal("24.009861")
    d15 = Decimal("25.143565")
    d = d11 + d12 + d13 + d14 + d15
    #d = int(d * 1000000)
    n1 = round(d * 2 / 3,6)
    print(n1)
    n2 = round(d / 3,6)
    print(n2)
    #d_1 = d * 2 / 3
    #d_2 = d / 3
    #print(d)
    #print(d16_1 + d16_2)
    #print(d_1 + d_2)
    #TestWork()
    TestAmount()