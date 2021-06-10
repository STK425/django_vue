# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json, codecs, os, csv


class SpiderCctvPipeline:
    def process_item(self, item, spider):
        return item

# 保存为csv文件
class Pipiline_ToCSV(object):
    content = open(os.path.dirname(__file__) + '/spiders/repeat.txt', encoding='utf_8').read()
    repeat = open(os.path.dirname(__file__) + '/spiders/repeat.txt', 'w', encoding='utf_8')
    repeat.write(content)

    def __init__(self):
        #文件的位置
        store_file = os.path.dirname(__file__) + '/spiders/cctv.csv'
        #打开文件，并设置编码
        self.file = codecs.open(filename= store_file, mode= 'wb', encoding='utf_8_sig')

        # 写入csv
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        line = (item['title'], item['url'], item['source'], item['timestamp'], item['detail'])
        # 逐行写入
        if item['detail'] != '':
            self.writer.writerow(line)
            self.repeat.write(item['url'] + r'||')
        return item

    def close_spider(self, spider):
        self.repeat.close()
        self.file.close()
