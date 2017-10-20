# -*- coding: utf-8 -*-
import scrapy
import html
from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

from Crawler_project.items import CrawlerProjectItem
from bs4 import BeautifulSoup

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AdviceAllitem2Spider(scrapy.Spider):
    name = 'advice_allitem_2'
    allowed_domains = ['advice.co.th']
    start_urls = ['http://www.advice.co.th/pricelist/']

    def parse(self, response):
        main_loops = Selector(response).xpath('//main[contains(@class,"main")]/section[2]/div[3]/div/div[1]/div/ul/li')
        x = ""
        # check = 0
        # outside loop ( main type )
        for loop in main_loops:
            loop_1 = loop.xpath('a/text()').extract_first()
            if loop_1 is None :
                loop_1 = x
            x = loop_1
            # for type in types
            loop_2 = loop.xpath('a/@data-content').extract_first()
            soup = BeautifulSoup(''.join(loop_2), 'html.parser')

            for in_loop in soup.find_all('li'):
                if in_loop is None:
                    continue
                data_typemain = x
                urls = in_loop.a['href']
                data_type = in_loop.get_text()
                next_page = response.urljoin(urls)

                # check+=1
                # yield {
                #     'typemain': data_typemain.strip(),
                #     'type': data_type.strip(),
                #     'url' : urls,
                #     'check' : check
                # }

                yield scrapy.Request(next_page, callback=self.parse_dir_contents, meta={
                    'typemain': data_typemain.strip(),
                    'type': data_type.strip()
                })

    def parse_dir_contents(self, response):
        # contents = Selector(response).xpath('//html/body/div[2]/div/div/div/div/div[3]/div[1]/div[4]/div[not(@id)]/div/table/tbody/tr')

        data = Selector(response).xpath("// main / section[2] / div[3] / div / div[2] / div / div[3] / div[contains(@class,'table-responsive')]")
        for sub_data in data:
            url = sub_data.xpath('table / tbody / tr / td[2]/ a / @href').extract()
            name = sub_data.xpath('table / tbody / tr / td[2]/ a / text()').extract()
            detail = sub_data.xpath("table / tbody / tr / td[3] / div[contains(@class,'entry-tb-content')] / p / text()").extract()
            price = sub_data.xpath("table / tbody / tr / td[contains(@class,'price')] / text()").extract()
            warranty = sub_data.xpath("table / tbody / tr / td[contains(@class,'waranty')] / text()").extract()

            for content in zip(url, name, detail, price, warranty):
                next_page = response.urljoin(content[0])
                yield scrapy.Request(next_page, callback=self.parse_dir_detail, meta={
                    'type_main': response.meta['typemain'],
                    'type': response.meta['type'],
                    'name' : content[1].strip(),
                    'detail' : content[2].strip(),
                    'price' : content[3].strip(),
                    'warranty' : content[4].strip(),
                    'url': content[0],
                   })

    def parse_dir_detail(self, response):
        check = Selector(response).xpath("//div[contains(@id,'pd_spec')]/table/tbody/tr[1]/td[1] /text()").extract_first().strip()
        if (check == 'Brand'):
            company = Selector(response).xpath("//div[contains(@id,'pd_spec')]/table/tbody/tr[1]/td[2] /text()").extract_first().strip()
        else:
            company = 'no brand'
        item = CrawlerProjectItem()
        if (response.meta['warranty'] is None):
            item['warranty'] = "no warranty"
        else:
            item['warranty'] = response.meta['warranty']
        # item['warranty'] = response.meta['warranty']
        item['url'] = response.meta['url']
        item['price'] = response.meta['price']
        item['details'] = response.meta['detail']
        item['type_main'] = response.meta['type_main']
        item['type'] = response.meta['type']
        item['name'] = response.meta['name']
        item['company'] = company
        yield item


