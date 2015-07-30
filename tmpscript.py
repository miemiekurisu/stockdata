import psycopg2
import sys
from uuid import uuid1
import time
import datetime
import ConfigParser
import crud
import urllib2
import logging

def getDbConfig():
    config = ConfigParser.ConfigParser()
    with open('dbinfo.cfg','r') as cfgfile:
       config.readfp(cfgfile)
    return config

def select(config,tablename, querystr ):
    db = config.get('database','dbname')
    usr = config.get('database','user')
    pswd = config.get('database','password')
    hostaddr = config.get('database','host')
    select = "select productid from tbl_stock_code"
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr)
        cur = con.cursor()
        cur.execute(select)    
        return cur.fetchall()
    except psycopg2.DatabaseError, e:    
        print 'Error %s' % e    
        sys.exit(1)
    finally:
        if con:
            con.close()

url_fmt = 'http://quotes.money.163.com/service/chddata.html?code=0%s&start=19980101&end=20150729&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

insertnames = ['TRADDATE'  , 'PRODUCTID'  , 'PRODUCTNAME','closingprice'  , 'highestprice'  , 'lowestprice'  , 'oPENING' , 'LASTCLOSE'  , 'ChangeAmount'  , 'Quotechange'  , 'turnoverratio' , 'dailyvolume'  , 'TurnoverTotal'  ,'totalmarketcapitalization' , 'floatmarketcapitalization']

 
cfg = getDbConfig()
crud.initTables(cfg)
row = select(cfg,'tbl_stock_code',None)

for i in row:
    url =  url_fmt%i[0]
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    historycsv = response.read().decode('gbk').splitlines()
    for i in historycsv[1:-1]:
        hisdata = dict(zip(insertnames,i.replace("'","").split(',')))
        crud.insertOne(cfg,'tbl_trade_history',hisdata)
    