# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request, FormRequest
from scrapy.selector import Selector

from Crawler_project.items import CrawlerProjectItem

class AdviceAllitemSpider(Spider):
    name = 'advice_allitem'
    allowed_domains = ['advice.co.th']
    start_urls = ['http://www.advice.co.th/pricelist/']

    def parse(self, response):
        mains = Selector(response).xpath('//html/body/div[2]/div/div/div/div/div[2]/ul/li')
        # yield mains
        # item = CrawlerProjectItem()
        x = ""
        for main in mains:
            # item = CrawlerProjectItem()
            data_typemain = main.css('a.main-menu > div.menu-text.font-bold::text').extract_first()
            # item['type_main'] = main.select('normalize-space(//a[contains(@class,"main-menu")]/div[contains(@class,"menu-text font-bold")]/text())').extract_first()

            # item['type_main'] = main.select('//a[contains(@class,"main-menu")]/div[contains(@class,"menu-text font-bold")]/text()').extract()[0].strip()
            # select('normalize-space(.//td[@scope="row"])').extract()[0].strip()
            if data_typemain is None :
                data_typemain = x
            x = data_typemain
            # for type in types
            data_type = main.css('a.pricelist-menu > div.menu-text::text').extract_first()

            # item['url'] = item['type_main'].stirp()
            if data_type is None:
                continue
            # item['type'] = main.xpath('/a[contains(@class,"pricelist-menu")]/div[contains(@class,"menu-text")]/text').extract_first()
            urls = main.xpath('a[contains(@class,"pricelist-menu")]/@href').extract_first()
            # request = Request( url, callback=self.parse_contents )
            # request = scrapy.Request(url, callback=self.parse_contents)
            # yield {
            #     'main_type':data_typemain.strip(),
            #     'type': data_type.strip(),
            #     'url': url
            #     }
            # request.meta['typemain'] = data_typemain.strip()
            #
            # request = Request(url[0], callback=s/elf.parse_dir_contents)
            # # request.meta['item1'] = item
            # yield request
            # yield request
            next_page = response.urljoin(urls)
            yield scrapy.Request(next_page, callback=self.parse_dir_contents, meta = {
                'typemain' : data_typemain.strip(),
                'type' : data_type.strip()
            })

    def parse_dir_contents(self, response):
        # contents = Selector(response).xpath('//html/body/div[2]/div/div/div/div/div[3]/div[1]/div[4]/div[not(@id)]/div/table/tbody/tr')
        url = Selector(response).xpath('//td[contains(@class, "pricelist-border-right pricelist-td pricelist-td valign-center click-row")]/@data-href').extract()
        name = Selector(response).xpath('//span[contains(@class,"pl-data-pdname")]/text()').extract()
        detail = Selector(response).xpath('//td[(@title)]/div[contains(@class,"pricelist-item-data")]/div[contains(@class,"pl-data")]/span/text()').extract()
        price = Selector(response).xpath('//td[contains(@align,"center")]/div[contains(@class,"pricelist-item-data")]/span[contains(@style,"color: #333333;")]/text()').extract()
        warrantly = Selector(response).xpath('//td[contains(@class,"pricelist-border-right pricelist-td pricelist-td valign-center click-row")]/div[contains(@class,"pricelist-item-data")]/text()').extract()
        for content in zip(url,name,detail,price,warrantly):
            # yield { 'url' : content[0],
            #         'name' : content[1],
            #         'detail' : content[2].strip(),
            #         'type' : response.meta['type'],
            #         'type_main' : response.meta['typemain'],
            #         'price' : content[3],
            #         'warrantly' : content[4].strip()
            #        }
            next_page = response.urljoin(content[0])
            yield scrapy.Request(next_page, callback=self.parse_dir_detail, meta={
                    'url' : content[0],
                    'name' : content[1],
                    'detail' : content[2].strip(),
                    'type' : response.meta['type'],
                    'type_main' : response.meta['typemain'],
                    'price' : content[3],
                    'warrantly' : content[4].strip()
            })

        # for content in contents:
            # item = CrawlerProjectItem()
            # item['url'] = content.xpath('td[2]/@data-href').extract_first()
        #     # item['details'] = Field()
        #     # item['img'] = Field()
        #     # item['details'] = Field()
        #     # item['details'] = Field()
        #     # item['url'] = Field()
        #     # item['details'] = Field()
        #     item['type_main'] = response.meta['typemain']
        #     item['type'] = response.meta['type']
        #
        #     # item = response.meta['data']
        #     # item['content'] = sel.xpath('tr/td/a/text()').extract_first()
        #     yield {
        #         'typemain' : x,
        #         'type' : y
        #     }
        #     yield item
        #     self.logger.info("Visited %s", response.url)
        # self.logger.info("Visited %s "
        #                  "type :  %s "
        #                  "typemain : %s", response.url,response.meta['type'], response.meta['typemain'])

    def parse_dir_detail(self, response):
        company = Selector(response).xpath('//table[contains(@id,"prod1")]/tr[1]/td[2]/div/text()').extract_first().strip()
        item = CrawlerProjectItem()
        item['warrantly'] = response.meta['warrantly']
        item['url'] = response.meta['url']
        item['details'] =response.meta['detail']
        item['type_main'] = response.meta['type_main']
        item['type'] = response.meta['type']
        item['name'] = response.meta['name']
        item['company'] = company
        yield item