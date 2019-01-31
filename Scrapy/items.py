# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Join


class ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CarItem(scrapy.Item):
    tag = scrapy.Field()
    comment = scrapy.Field()


class DoubanBookItem(scrapy.Item):
    ISBN = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field(
        output_processor=Join(",")
    )
    publishing_house = scrapy.Field()
    rating = scrapy.Field()
    tag = scrapy.Field(
        output_processor=Join(",")
    )
    rec_book = scrapy.Field(
        output_processor=Join(",")
    )


class DoubanReviewItem(scrapy.Item):
    title = scrapy.Field()
    review = scrapy.Field(
        output_processor=Join(",")
    )


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    specification = scrapy.Field()
    texture = scrapy.Field()
    weight = scrapy.Field()
    introduction = scrapy.Field()
    img_url = scrapy.Field()