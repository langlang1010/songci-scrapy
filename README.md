## 宋词学习网站-数据获取

使用的是scrapy框架，用来爬虫数据。

### 基本流程
以下的内容是从开发者的角度进行编写的。
1. 安装scrapy
  ```bash
  pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple 
  ```
2. 初始化项目
  ```bash
  scrapy startproject tutorial
  ```
3. 配置项目
  找到 `tutorial/settings.py` 文件中以下内容，然后去掉前面的注释符。
  ```bash
  ITEM_PIPELINES = {
      'tutorial.pipelines.TutorialPipeline': 300,
  }
  ```
4. 编辑 `tutorial/items.py`
  修改 `TutorialItem`类，修改后如下内容:
  ```python
  class TutorialItem(scrapy.Item):
      # define the fields for your item here like:
      # 词名（含词牌名）
      name = scrapy.Field()
      # 时期
      dynasty = scrapy.Field()
      # 作者
      author = scrapy.Field()
      # 内容
      content = scrapy.Field() 
      # 翻译
      explanation = scrapy.Field() 
      # 注释
      note = scrapy.Field()  
  ```
5. 编辑 `tutorial\spiders\quotes_spider.py` 文件
  可以认为这里是爬虫的开始，需要配置目标网址，并且编写相应的处理逻辑，数据流向。
  ```python
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
          ...
  ```
  运行到这里数据已经通过yield存储起来了，接下来通过编辑pipline来把数据存储到MySQL中。
6. 编辑 `tutorial\pipelines.py` 文件
  这里是最后的处理，把数据存储到MySQL中去，代码如下：
  ```python
  import mysql.connector

class TutorialPipeline(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="smileyan.cn",
          port=3306,
          user="root",
          passwd="password",
          database="songci"
         )
        
        
    def process_item(self, item, spider):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#         print(item['name'])
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO content(title, name, author, dynasty, content) VALUES (%s, %s, %s, %s, %s)"
        temp = str(item['name']).split('·')
        val = (temp[0], temp[1], str(item['author']), str(item['dynasty']), str(item['content']))
        mycursor.execute(sql, val)
        ...
  ```
### 项目相关
* 前端源码地址：https://github.com/langlang1010/songci-client/
* 后端源码地址：https://github.com/langlang1010/songci/

### 总结
此模块的内容非常简单（可能是因为目标网址并没有做相关防护），准要需要查一下文档，检查目标地址的源码来确定 `xpath` 代码。
  
  
  
