# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import logging
from scrapy.item import Item, Field


class ArxivOrgItem(scrapy.Item):
    article_link = Field()
    article_title = Field()
    article_authors = Field()
    article_published_date = Field()
    article_abstract = Field()
    article_pdf_link = Field()

    def get_insert_sql(self):
        insert_sql = 'INSERT INTO arxiv_article(article_link, article_title, article_authors, article_published_date, article_abstract, article_pdf_link) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (
                 self['article_link'],
                 self['article_title'],
                 self['article_authors'],
                 self['article_published_date'],
                 self['article_abstract'],
                 self['article_pdf_link']
                 )
        return insert_sql, params
