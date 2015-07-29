#!/usr/bin/python
# -*- coding: utf-8 -*-

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


def initTables(config):
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

def deleteData(config,tablename,query=None):
    db = config.get('database','dbname')
    usr = config.get('database','user')
    pswd = config.get('database','password')
    hostaddr = config.get('database','host')
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr) 
        cur = con.cursor()
        sql = None
        if query==None:
            sql = "delete from %s "%tablename
        else:
            sql = "delete from %s where %s"%(tablename,query)
        cur.execute(sql)    
        con.commit()
    except psycopg2.DatabaseError, e:    
        if con:
            con.rollback()    
        print 'Error %s' % e    
        sys.exit(1)
    finally:
        if con:
            con.close()
            
def insertOne(config,tablename,jsondata):
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

def batchInsert(config,tablename,jsonlist):
    db = config.get('database','dbname')
    usr = config.get('database','user')
    pswd = config.get('database','password')
    hostaddr = config.get('database','host')
    
    insertDate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # insert = "INSERT INTO %s (id,%s,CREATETIME) VALUES('%s','%s','%s')"%(tablename,','.join(jsondata.keys()),uuid1(),"\',\'".join(jsondata.values()),insertDate)
    try:
        con = psycopg2.connect(database=db,user=usr,password=pswd,host=hostaddr)
        cur = con.cursor()
        for i in range(1,len(jsonlist)):
            if i%100==0:
                con.commit()
            insert = "INSERT INTO %s (id,%s,CREATETIME) VALUES('%s','%s','%s')"%(tablename,','.join(jsonlist[i].keys()),uuid1(),"\',\'".join(jsonlist[i].values()),insertDate)
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
        retrun cur.fetchall()
    except psycopg2.DatabaseError, e:    
        print 'Error %s' % e    
        sys.exit(1)
    finally:
        if con:
            con.close()

def convToInsertValues(jsonstr):
    sqlstr = []
    for i in jsonstr.keys():
        sqlstr.append("%s='%s'"%(i,jsonstr.get(i)))
    return ','.join(sqlstr)
