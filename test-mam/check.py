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
from operator import itemgetter, attrgetter

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

def TestAmount():
    BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT = 5
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).all()
    info = {}
    for tx in Txs:
        if tx.height not in info:
            info[tx.height] = {
                "work":None,
                "stake":None,
                "distribute":[],
                "vote":[]}
        if tx.type == 'work':
            info[tx.height]["work"] = tx
        if tx.type == 'stake':
            info[tx.height]["stake"] = tx
        if tx.type == 'distribute':
            info[tx.height]["distribute"].append(tx)
        if tx.type == 'token' and tx.sendto[0:4] == "21c0":
            info[tx.height]["vote"].append(tx)


    N_ = Decimal("100")
    M_ = N_ * 100
    TotalReward = Decimal("0")
    MoneySupply = Decimal("0")
    Vote = {}
    Stakes = []
    for obj in info:
        TotalReward = TotalReward + Decimal("100.0")
        MoneySupply = MoneySupply + Decimal("38.2")
        Stake = 0

        if info[obj]["work"].sendto in Vote:
            if Vote[info[obj]["work"].sendto] > M_:
                Stake = round((TotalReward - MoneySupply),6)
            else:
                Stake = round((TotalReward - MoneySupply) * Vote[info[obj]["work"].sendto] / M_,6)
        Stakes.append(Stake)
        MoneySupply = MoneySupply + Stake
        assert Stake == info[obj]["stake"].amount,"stake 金额错误"

        height = info[obj]["work"].height
        if height % BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT == 1:
            sum_ = Decimal("0")
            for d in info[obj]["distribute"]:
                sum_ += d.amount

            #for d in info[obj]["distribute"]:
            #    print(d.sendto,d.amount / sum_)
            #print("--------------------",height)
            sum2_ = sum(Stakes[:-1])
            assert sum_ == sum2_,"奖励发放错误"
            Stakes = Stakes[-1:]

        for tx in info[obj]["distribute"]:
            if tx.pool_in in Vote:
                Vote[tx.pool_in] += tx.amount
            else:
                Vote[tx.pool_in] = tx.amount

        for tx in info[obj]["vote"]:
            if tx.pool_in in Vote:
                Vote[tx.pool_in] += tx.amount
            else:
                Vote[tx.pool_in] = tx.amount

    session.close()
    print("TestAmount OK")

if __name__ == '__main__':
    #TestWork()
    TestAmount()