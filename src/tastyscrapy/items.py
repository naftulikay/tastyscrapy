#!/usr/bin/env python3

import scrapy


class Bookmark(scrapy.Item):
    """A Delicious bookmark item."""

    delicious_id = scrapy.Field()
    created = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    comment = scrapy.Field()
    tags = scrapy.Field()
    private = scrapy.Field()
