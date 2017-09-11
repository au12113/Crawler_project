# -*- coding: utf-8 -*-
# import scrapy
from scrapy import Spider, Request
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.spiders import XMLFeedSpider

from Crawler_project.items import CrawlerProjectItem
class AdviceSpider(XMLFeedSpider):

    name = 'advice'
    allowed_domains = ['templehealth.org']
    start_urls = ['https://hr.templehealth.org/hrapp/rss/careers_jo_rss.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'


    # def parse(self, response):
    #     # pass
    #     x = HtmlXPathSelector(response)
    #     x.register_namespace("g", "http://www.sitemaps.org/schemas/sitemap/0.9")
    #     x.select("//g:loc").extract()
    #     for loc in x:
    #         item = CrawlerProjectItem()
    #         item['url'] = x.select("//g:loc").extract()
    #         yield item

    def parse_node(self, response, node):
        title = node.xpath('//title/text()').extract()
        link = node.xpath('link/text()').extract()
        pubdate = node.xpath('item/pubDate/text()').extract()
        category = node.xpath('item/category/text()').extract()
        item = CrawlerProjectItem()
        item['title'] = title
        item['link'] = link
        item['pubdate'] = pubdate
        item['category'] = category
        yield item