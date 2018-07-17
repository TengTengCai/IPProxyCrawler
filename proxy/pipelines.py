# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import redis
from redis import ConnectionError, TimeoutError


class ProxyPipeline(object):
    def __init__(self):
        self.redis_client = redis.Redis(host='120.79.52.3',
                                        port='8464',
                                        password='yxgw')

    def process_item(self, item, spider):
        try:
            self.redis_client.lpush('proxy_info_pool', item['proxy_info'])
            self.redis_client.expire('proxy_info_pool', 86400)
        except (ConnectionError, TimeoutError) as e:
            logging.error(e)
        return item
