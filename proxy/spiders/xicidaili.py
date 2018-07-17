# -*- coding: utf-8 -*-
import json

import scrapy

from proxy.items import ProxyItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['www.xicidaili.com']

    def start_requests(self):
        base_url = 'http://www.xicidaili.com/'
        for keyword in ['nn', 'nt', 'wn', 'wt']:
            for page in range(1, 5):
                full_url = str(f'{base_url}{keyword}/{page}')
                yield scrapy.Request(url=full_url, callback=self.parse)

    def parse(self, response):
        trs1 = response.xpath('//tr[@class=""]')
        trs2 = response.xpath('//tr[@class="odd"]')
        trs = trs1 + trs2
        for tr in trs:
            p_type = tr.xpath('td[6]/text()').extract_first()
            p_type = 'http' if p_type == 'HTTP' else 'https'
            data = {'ip': tr.xpath('td[2]/text()').extract_first(),
                    'port': tr.xpath('td[3]/text()').extract_first(),
                    'anonymity': tr.xpath('td[5]/text()').extract_first(),
                    'p_type': p_type,
                    'p_address': tr.xpath('td[4]/a/text()').extract_first()}
            item = ProxyItem()
            item['proxy_info'] = json.dumps(data)
            yield item
