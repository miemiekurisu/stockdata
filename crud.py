#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
from uuid import uuid1
import time
import datetime

def getdbconfig():
    config = ConfigParser.ConfigParser()
    with open('dbinfo.cfg','r') as cfgfile:
       config.readfp(cfgfile)
    return config

def inittables(config):
    db = config.get('database','dbname')
    usr = config.get('database','user')
    pswd = config.get('database','password')
    hostaddr = config.get('database','host')
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr) 
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tbl_stock_code(Id varchar(100) PRIMARY KEY, PRODUCTID varchar(20), FULLNAME varchar(200), NUM varchar(10), PRODUCTNAME varchar(200), CREATETIME varchar(200))")    
        con.commit()
    except psycopg2.DatabaseError, e:    
        if con:
            con.rollback()    
        print 'Error %s' % e    
        sys.exit(1)
    finally:
        if con:
            con.close()

def insertData(config,tablename,jsondata):
    db = config.get('database','dbname')
    usr = config.get('database','user')
    pswd = config.get('database','password')
    hostaddr = config.get('database','host')
    insert = "INSERT INTO %s (id,%s,CREATETIME) VALUES('%s','%s','%s')"%(tablename,','.join(jsondata.keys()),uuid1(),"\',\'".join(jsondata.values()),datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr)
        cur = con.cursor()
        cur.execute(insert)    
        con.commit()
    except psycopg2.DatabaseError, e:    
        if con:
            con.rollback()    
        print 'Error %s' % e    
        sys.exit(1)
    finally:
        if con:
            con.close()
            
def convtoinsertvalues(jsonstr):
    sqlstr = []
    for i in jsonstr.keys():
        sqlstr.append("%s='%s'"%(i,jsonstr.get(i)))
    return ','.join(sqlstr)
