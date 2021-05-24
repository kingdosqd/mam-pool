#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 3.6.9
# sqlalchemy 1.4.15(sqlalchemy.__version__)
'''
检查项:
1:pow奖励金额的正确性
'''

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR,DECIMAL
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal,getcontext
import sqlalchemy


Base = declarative_base()

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
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/minemon", encoding="utf-8")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Txs = session.query(Tx).filter(Tx.type == 'work').all()
    height = 1
    for tx in Txs:
        if tx.amount != Decimal('38.2') or height != tx.height:
        #if height != tx.height:
            print("TestWork err:",tx.height,tx.amount,tx.txid)
            exit()
        height = height + 1
    session.close()
    print("TestWork OK")

if __name__ == '__main__':
    print(sqlalchemy.__version__)
    TestWork()