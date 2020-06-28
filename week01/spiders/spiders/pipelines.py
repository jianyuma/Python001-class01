# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pandas as pd

class SpidersPipeline(object):
    def process_item(self, item, spider):
        df = pd.DataFrame(dict(item), index=[0])
        if os.path.exists('./my_scrapy.csv'):
            header = False
        else:
            header = True
        df.to_csv('./my_scrapy.csv', mode='a', index=False, header=header)
        return item