# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import openpyxl
import pymysql


# 钩子函数(方法) --> 回调方法 --> callback
class Spider2206ExcelPipeline:
    def __init__(self):
        #     初始化方法
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'Top250'
        self.ws.append(('标题', '评分', '主题'))

    # 爬虫开始做的事情（只会调用一次）
    def open_spider(self, spider):
        pass

    # 爬虫关闭时候做的事情（只会调用一次）
    def close_spider(self, spider):
        self.wb.save('电影数据.xlsx')

    # 爬虫拿到数据时候执行的函数(每拿到一条数据就会调用一次)
    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        self.ws.append((title, rank, subject))
        return item


class Spider2206DBPipeline:
    def __init__(self):
        #     初始化方法
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='douban', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.data = []

    # 爬虫关闭时候做的事情（只会调用一次）
    def close_spider(self, spider):
        if len(self.data)>0:
            self._write_to_db()
        self.cursor.close()

    # 爬虫拿到数据时候执行的函数(每拿到一条数据就会调用一次)
    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        self.data.append((title,rank,subject))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        self.conn.close()
        # self.cursor.execute(
        #     'insert into douban_top250(title, rank, subject) values(%s, %s, %s)',(title,rank,subject)
        # )
        return item

    def _write_to_db(self):
        self.cursor.executemany(
            'insert into douban_top250(title, rank, subject) values(%s, %s, %s)',
            self.data
        )
        self.conn.commit()
