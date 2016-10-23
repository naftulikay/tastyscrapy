#!/usr/bin/env python3

from scrapy.exceptions import DropItem
from tastyscrapy import model
from tastyscrapy.items import Bookmark


class DatabasePipeline(object):

    def open_spider(self, spider):
        """Callback on spider creation, used to setup SQLAlchemy."""

    def process_item(self, item, spider):
        """Callback on item returned from spider."""
        if type(item) is Bookmark:
            pass
        else:
            # not sure what this is, can't save it
            spider.logger.warn("Unknown item of type {}", type(item))
            raise DropItem

    def save_bookmark(self, bookmark, spider):
        """Saves or updates a bookmark to SQLAlchemy."""
        # ie model.Bookmark(...).save_or_update()
        # ie model.Tag(...).save_or_update()
