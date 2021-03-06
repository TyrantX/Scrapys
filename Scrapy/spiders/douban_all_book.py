# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from Scrapy.items import DoubanAllBookItem


class DoubanSpider(scrapy.Spider):
    name = 'douban_all_book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=cloud']

    def parse(self, response):
        tags = response.css('.tagCol tr td a::attr(href) ').extract()
        douban_url = "https://book.douban.com"
        for tag in tags:
            yield Request(url=parse.urljoin(douban_url, tag), callback=self.parse_tag)

    def parse_tag(self, response):
        # 获取所有标签下的书籍url并交给scrapy下载后进行解析
        post_nodes = response.css('.subject-item .info')
        for post_node in post_nodes:
            title = post_node.css('h2 a::attr(title)').extract()
            book_info = post_node.css('.pub::text').extract()
            # rating_nums = post_node.css('.star .rating_nums::text').extract_first('')
            post_url = post_node.css('h2 a::attr(href)').extract_first('')
            douban_id = post_url.split('/', 5)[-2]

            book_item = DoubanAllBookItem()

            book = book_info[0].replace('\n', '').strip().split('/')
            authors = book[0]
            publishing_house = book[-3]

            item_loader = ItemLoader(item=DoubanAllBookItem(), response=response)
            item_loader.add_value("douban_id", douban_id)
            item_loader.add_value("title", title)
            item_loader.add_value("author", authors)
            item_loader.add_value("publishing_house", publishing_house)

            book_item = item_loader.load_item()

            yield book_item

        # 获取下一页url并继续交给scrapy下载
        next_url = response.css('.next a::attr(href)').extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse_tag)

    # def parse_detailed(self, response):
    #     # 提取文章详情页的具体字段：书名 作者 出版社 关键词 分类 评分 喜欢这本书的人还喜欢什么
    #     book_item = DoubanBookItem()
    #     rec_book_list = []
    #
    #     book_info = response.meta["book_info"]
    #     douban_id = response.meta["id"]
    #
    #     book = book_info[0].replace('\n', '').strip().split('/')
    #     authors = book[0]
    #     publishing_house = book[-3]
    #     title = response.css('#wrapper h1 span::text').extract()[0]
    #     # rating = response.css('.rating_self strong::text').extract()[0].strip()
    #     # tag = response.css('.indent span .tag::text').extract()
    #     rec_books = response.css('#db-rec-section .content dl dd a::text').extract()
    #     for rec_book in rec_books:
    #         rec_book.replace('\n', '').strip()
    #         rec_book_list.append(rec_book.replace('\n', '').strip())
    #
    #     item_loader = ItemLoader(item=DoubanBookItem(), response=response)
    #     item_loader.add_value("id", douban_id)
    #     item_loader.add_value("title", title)
    #     item_loader.add_value("author", authors)
    #     item_loader.add_value("publishing_house", publishing_house)
    #     # item_loader.add_css("rating", ".rating_self strong::text")
    #     # item_loader.add_css("tag", ".indent span .tag::text")
    #     # item_loader.add_value("rec_book", rec_book_list)
    #
    #     book_item = item_loader.load_item()
    #
    #     yield book_item
