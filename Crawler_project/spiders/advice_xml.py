# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from Crawler_project.items import CrawlerProjectItem

class AdviceXmlSpider(XMLFeedSpider):
    name = 'advice_xml'
    allowed_domains = ['advice.co.th']
    start_urls = ['https://www.advice.co.th/sitemap.xml']
    namespaces = [
        ('x', 'http://www.sitemaps.org/schemas/sitemap/0.9'),
    ]
    iterator = 'xml' # you can change this; see the docs
    itertag = 'x:loc' # change it accordingly

    def parse_node(self, response, node):
        # i = {}
        # #i['url'] = selector.select('url').extract()
        # #i['name'] = selector.select('name').extract()
        # #i['description'] = selector.select('description').extract()
        # return i
        url = node.xpath('text()').extract()
        # link = node.select('link/text()').extract()
        # pubdate = node.select('pubDate/text()').extract()
        # category = node.select('category/text()').extract()
        item = CrawlerProjectItem()
        item['url'] = url
        # item['link'] = link
        # item['pubdate'] = pubdate
        # item['category'] = category
        return item
        # self.logger.debug(node.xpath('text()').extract_first())