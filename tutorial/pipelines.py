# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class TutorialPipeline(object):
    def __init__(self):
        self.mydb = mysql.connector.connect(
          host="smileyan.cn",
          port=3306,
          user="root",
          passwd="Yan1996>",
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
        added_id = mycursor.lastrowid
        
        sql2 = "INSERT INTO supplement(id, explanation, note) VALUES(%s,%s,%s)"
        val2 = (str(added_id), str(item['explanation']),str(item['note']))
        mycursor.execute(sql2, val2)
        self.mydb.commit() 
        return item
    
