import scrapy
from tutorial.items import TutorialItem 
from tqdm import tqdm
import json
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        url = "https://www.gushiwen.org/gushi/songci.aspx"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        results = response.xpath('//div[@class="typecont"]/span/a/@href')
        urls = []
        for result in results:
            urls.append(result.get())

        # for each url
        with tqdm(total=len(urls)) as pbar:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse2)
                pbar.update(1)

    def parse2(self, response):
        item = TutorialItem()
        item['name'] = response.xpath('//h1/text()').get()
        item['dynasty'] = response.xpath('//p[1][@class="source"]/a[1]/text()').get()
        item['author'] = response.xpath('//p[1][@class="source"]/a[2]/text()').get()
        content = str(response.xpath('//div[@class="contson"]').get()).replace('<br>','br').replace('<br/>','br').replace('<p>','p').replace('\n','')
        # 去掉其他html 标签
        dr = re.compile(r'<[^>]+>',re.S)
        content = dr.sub('',content)
        item['content'] = content
        item['name'] = response.xpath('//h1/text()').get()
        # 翻译
        xpath_fangyi = "//div[@class='sons'][2]/div[@class='contyishang']"
        item['explanation'] = response.xpath(xpath_fangyi).get()
        # 获得翻译 ID
        fanyiIdTemp = item['explanation'].split("fanyiShow")
        if(len(fanyiIdTemp)>=2):
            fanyiId = fanyiIdTemp[1]
            fanyiId = fanyiId.split('\'')[1]
            item['explanation'] = fanyiId
            url = "https://so.gushiwen.org/nocdn/ajaxfanyi.aspx?id=" + fanyiId
            yield scrapy.Request(url=url, callback=self.parse3, meta={'item':item})
        else:
            # 对翻译和注释进行处理
            body = response.xpath("//div[@class='contyishang']/p[1]").get()
            item['explanation'] = self.rm_html_tag(body)
            body = response.xpath("//div[@class='contyishang']/p[2]").get()
            item['note'] = self.rm_html_tag(body)
            yield item
            
    def parse3(self, response):
        item = response.meta['item']
        body = response.xpath("//div[@class='contyishang']/p[1]").get()
        item['explanation'] = self.rm_html_tag(body)
        body = response.xpath("//div[@class='contyishang']/p[2]").get()
        item['note'] = self.rm_html_tag(body)
        yield item
        
    def rm_html_tag(self, content):
        temp = str(content).replace('<br>','br').replace('<br/>','br').replace('<p>','p').replace('\n','')
        dr = re.compile(r'<[^>]+>',re.S)
        return dr.sub('',temp)
        