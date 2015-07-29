import psycopg2
import sys
from uuid import uuid1
import time
import datetime
import ConfigParser

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

bigcsv = []

for i in row[0:10]:
    url =  url_fmt%i[0]
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    bigcsv.append(response.read())