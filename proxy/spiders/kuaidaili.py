# -*- coding: utf-8 -*-
import json

import scrapy

from proxy.items import ProxyItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['www.kuaidaili.com']

    def start_requests(self):
        base_url = 'https://www.kuaidaili.com/free/'
        for anonymity in ('inha', 'intr'):
            for page in range(10):
                full_url = str(f'{base_url}{anonymity}/{page}/')
                yield scrapy.Request(url=full_url, callback=self.parse)

    def parse(self, response):
        tbody = response.xpath('/html/body/div[1]/div[4]/div[2]/div/div[2]/table/tbody//tr')
        for tr in tbody:
            p_type = tr.xpath('td[4]/text()').extract_first().lower()
            p_type = 'http' if p_type == 'HTTP' else 'https'
            data = {'ip': tr.xpath('td[1]/text()').extract_first(),
                    'port': tr.xpath('td[2]/text()').extract_first(),
                    'anonymity': tr.xpath('td[3]/text()').extract_first(),
                    'p_type': p_type,
                    'p_address': tr.xpath('td[5]/text()').extract_first()}
            item = ProxyItem()
            item['proxy_info'] = json.dumps(data)
            yield item
