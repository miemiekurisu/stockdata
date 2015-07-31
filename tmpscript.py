import psycopg2
import sys
from uuid import uuid1
import time
from datetime import datetime
import ConfigParser
import crud
import urllib2
import logging
from uuid import uuid1

logging.basicConfig(filename='example.log',level=logging.INFO)


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
db = cfg.get('database','dbname')
usr = cfg.get('database','user')
pswd = cfg.get('database','password')
hostaddr = cfg.get('database','host')


        
for i in row:
    url =  url_fmt%i[0]
    logging.info('%s %s Begin'%(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),i[0]))
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    historycsv = response.read().decode('gbk').splitlines()
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr)
        cur = con.cursor()
        if len(historycsv) <=1:
            continue
        for i in historycsv[1:-1]:
            hisdata = dict(zip(insertnames,i.replace("'","").split(',')))
            insert = "INSERT INTO %s (id,%s,CREATETIME) VALUES('%s','%s','%s')"%(tablename,','.join(hisdata.keys()),uuid1(),"\',\'".join(hisdata.values()),datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            logging.debug(insert)
            cur.execute(insert)
        con.commit()
        logging.info('%s %s End'%(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),i[0]))
    except psycopg2.DatabaseError, e:    
        if con:
            con.rollback()    
        logging.error('%s Error %s' % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),e))     
        sys.exit(1)
    finally:
        if con:
            con.close()