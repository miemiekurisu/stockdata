'''
curl -i -H "Accept: */*" -H "Host:query.sse.com.cn" -H "Referer:http://www.sse.com.cn/assortment/stock/list/name/" "http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback49079&isPagination=true&sqlId=COMMON_SSE_ZQPZ_GPLB_MCJS_SSAG_L&pageHelp.pageSize=1&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.endPage=22&_=1437499711856"
'''
import urllib
import urllib2
import json
import codecs
import ConfigParser

def getconfig():
    config = ConfigParser.ConfigParser()
    with open('stockbaseinfo.cfg','r') as cfgfile:  
        config.readfp(cfgfile)
    return config

def geturl(config, productcode=None):
    url = []
    if productcode != None:
        for sqlid in config.get('stockdetail','sqlid').split(','):
            url.append(config.get('stockdetail','urldetail')%(sqlid,productcode))
    else:
        url.append(config.get('stockdetail','urlall'))
    return url


def getrawdata(config,url):
    user_agent = config.get('baseinfo','user_agent')
    accept = config.get('baseinfo','accept')
    refHost= config.get('baseinfo','refHost')
    referer = config.get('baseinfo','referer')
    headers = { 'User-Agent' : user_agent, 'Host':refHost, 'Referer':referer }
    req = urllib2.Request(url,None,headers)
    response = urllib2.urlopen(req)
    return response.read()

def getresult(rawdata):
    jsonstr = rawdata.decode('utf-8')
    jsonstr = jsonstr[jsonstr.find('(')+1:len(jsonstr)-1]
    js = json.loads(jsonstr,encoding='utf-8')
    return js.get('result')

def getHistoryData(config, url):
    pass

# def prepareStockData():
#     
#     config = ConfigParser.ConfigParser()
#     with open('stockbaseinfo.cfg','r') as cfgfile:  
#         config.readfp(cfgfile)
#     url = config.get('stockdetail','urlall')
#     #url=config.get('stockdetail','durl1')+'600000'
#     user_agent = config.get('baseinfo','user_agent')
#     accept = config.get('baseinfo','accept')
#     refHost= config.get('baseinfo','refHost')
#     referer = config.get('baseinfo','referer')
#     headers = { 'User-Agent' : user_agent, 'Host':refHost, 'Referer':referer }
#     req = urllib2.Request(url,None,headers)
#     response = urllib2.urlopen(req)
#     data = response.read()
#     jsonstr = data.decode('utf-8')
#     jsonstr = jsonstr[jsonstr.find('(')+1:len(jsonstr)-1]
#     js = json.loads(jsonstr,encoding='utf-8')
#     stockdata = js.get('result')
#     return stockdata
