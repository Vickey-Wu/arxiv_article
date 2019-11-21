# -*- coding: utf-8 -*-
import scrapy
import logging
import xmltodict
import json
import re
from arxiv_org.items import ArxivOrgItem
from scrapy.selector import XmlXPathSelector
from scrapy.http import Request
from scrapy.http import XmlResponse


class ArxivArticleSpider(scrapy.Spider):
    name = 'arxiv_article'
    allowed_domains = ['export.arxiv.org/rss/cs']
    start_urls = ['http://export.arxiv.org/rss/cs/']


    def parse(self, response):
        item = ArxivOrgItem()
        xxs = XmlXPathSelector(response)
        xxs.remove_namespaces()
        # 需要先将selector对象格式化成str
        xml_data = str(xxs.xpath('//link'))
        #logging.log(logging.INFO, xml_data)
        url_list = re.findall('http://arxiv.org/abs/\d+.\d+', xml_data)
        #logging.log(logging.INFO, url_list)
        for url in url_list:
            logging.log(logging.INFO, f'**************** crawling link: {url} ***************** ')
            yield Request(url=url, callback=self.parse_single_page, meta={'item': item}, dont_filter = True)

    def parse_single_page(self, response):
        item = response.meta['item']
        article_title = response.xpath('//h1[@class="title mathjax"]/text()').extract()[0]
        article_authors = ', '.join(response.xpath('//div[@id="abs"]//div[@class="authors"]/a/text()').extract())
        tmp_date = response.xpath('//div[@id="abs"]//div[@class="dateline"]/text()').extract()[0]
        article_published_date = re.findall('Submitted on\s(\d+\s\w+\s\d+)', tmp_date)
        article_abstract = response.xpath('//div[@id="content"]//div[@id="abs"]//blockquote/text()').extract()[0]
        logging.log(logging.INFO, '**************** article detail log ****************')
        item['article_link'] = response.url
        item['article_title'] = article_title
        item['article_authors'] = article_authors
        item['article_published_date'] = article_published_date
        item['article_abstract'] = article_abstract
        item['article_pdf_link'] = response.url.replace('abs', 'pdf')
        logging.log(logging.INFO, item['article_link'])
        logging.log(logging.INFO, article_title)
        logging.log(logging.INFO, article_authors)
        logging.log(logging.INFO, article_published_date)
        logging.log(logging.INFO, article_abstract)
        logging.log(logging.INFO, item['article_pdf_link'])
        yield item
