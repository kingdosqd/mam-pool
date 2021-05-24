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

def TestWork():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).filter(Tx.type == 'work').all()
    height = 1
    for tx in Txs:
        assert tx.amount == Decimal('38.2'),'TestWork amount(%f) err.height:%d' % (tx.amount,tx.height)
        assert height == tx.height,'TestWork height(%d) err.' % tx.height
        height = height + 1
    session.close()
    print("TestWork OK")

def TestAmount():
    BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT = 2
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).all()
    N_ = Decimal("100")
    M_ = N_ * 100
    TotalReward = Decimal("0")
    MoneySupply = Decimal("0")
    Vote = Decimal("0")
    Stakes = []
    for tx in Txs:
        if tx.type == 'work':
            TotalReward = TotalReward + Decimal("100.0")
            MoneySupply = MoneySupply + Decimal("38.2")
        if tx.type == 'stake':
            Stake = round((TotalReward - MoneySupply) * Vote / M_,6)
            assert tx.amount == Stake,"奖励金额不对.tx.amount:%f, Stake:%f, height:%d" % (tx.amount, Stake,tx.height)
            Stakes.append(Stake)
            MoneySupply = MoneySupply + Stake
        if tx.type == 'distribute':
            Vote = Vote + tx.amount
            if len(Stakes) == BBCP_PLEDGE_REWARD_DISTRIBUTE_HEIGHT + 1:
                assert tx.amount == sum(Stakes[:-1]),"系统发的奖励错误"
            Stakes = Stakes[-1:]
        if tx.sendto[0:4] == "21c0" and tx.type != "distribute":
            assert tx.amount >= Decimal("100"),"投票金额小于100（%f" % tx.amount
            Vote = Vote + tx.amount
    session.close()
    print("TestAmount OK")

if __name__ == '__main__':
    #TestWork()
    TestAmount()