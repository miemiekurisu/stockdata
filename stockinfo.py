import scrapy
import codecs
from fdata2.items import stockinfo
class StockInfoSprider(scrapy.Spider):
    name = "stockinfo"
    allowed_domains = ["sse.com.cn"]
    start_urls = ["http://biz.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStockInfoInitAct?reportName=BizCompStockInfoRpt&PRODUCTID=&PRODUCTJP=&PRODUCTNAME=&keyword=&tab_flg=&CURSOR=1"]
    '''
    def parse(self, response):
        nextlink = response.xpath('//*[@class="nextpage"]/a/@href').extract()
        nextpage=nextlink[len(nextlink)-1]    
        yield scrapy.Request(response.urljoin(nextpage),callback=self.parse_stockinfo)
    '''
    def parse(self,response):
        for stock in response.xpath('//*[@cellspacing="1" and @cellpadding="2"]/tr'):
            item = stockinfo()
            item['stockcode'] = stock.xpath('*[@class="table3" and @width="40%"]/a/text()').extract()
            item['stockname'] = stock.xpath('*[@class="table3" ]/text()').extract()
            yield item

        nextlink = response.xpath('//*[@class="nextpage"]/a/@href').extract()
        nextpage=nextlink[len(nextlink)-1]    
        yield scrapy.Request(response.urljoin(nextpage),callback=self.parse)

