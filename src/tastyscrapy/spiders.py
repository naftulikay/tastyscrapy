#!/usr/bin/env python3

from datetime import datetime
from tastyscrapy.exceptions import LoginFailedException
from tastyscrapy.items import Bookmark
from urllib import parse as urlparse

import json
import scrapy
import xjpath


class DeliciousSpider(scrapy.Spider):

    name = 'delicious'

    start_urls = ["https://del.icio.us/login"]

    def parse(self, response):
        """Default callback only used for initial login crawling."""
        return [
            scrapy.FormRequest.from_response(response,
                formdata={'username': self.settings.get('DELICIOUS_USERNAME'),
                          'password': self.settings.get('DELICIOUS_PASSWORD')},
                callback=self.on_login_response)
        ]

    def on_login_response(self, response):
        """
        Callback method triggered on response to a login attempt.

        Example response for a failed login attempt:
        http://pastebin.com/c4Skavpa

        Example response for a successful login attempt:
        http://pastebin.com/Ds2Gqykr
        """
        if response.status >= 400:
            raise LoginFailedException("Received response {} when trying to log in.".format(response.status))

        # create variable for storing the json payload
        payload = None

        try:
            payload = json.loads(response.text)
        except:
            raise LoginFailedException("Unable to parse JSON response.")

        if xjpath.path_lookup(payload, 'status') != ('success', True):
            raise LoginFailedException("Unable to log in using provided credentials.")

        # lookup redirect url
        redirect, is_success = xjpath.path_lookup(payload, 'redirect')

        # extract session key for cookie
        session_key, session_value = xjpath.XJPath(payload)['session'].split('=')

        # start parsing items
        yield scrapy.Request(redirect if is_success else "https://del.icio.us/{}".format(
            self.settings.get('DELICIOUS_USERNAME')), callback=self.on_bookmark_response,
            cookies = { session_key: session_value })

    def on_bookmark_response(self, response):
        """
        Callback method triggered when login has succeeded or the next
        bookmark page has been fetched.
        """
        # get all bookmark blocks on the page
        for bookmark_block in response.css('.profileMidpanel .articleThumbBlockOuter'):
            # presumably a md5 of the url or something
            bookmark_id = bookmark_block.css('::attr(md5)').extract_first()
            # unix integer in utc timezone
            bookmark_date = int(bookmark_block.css('::attr(date)').extract_first())
            bookmark_title = bookmark_block.css('.articleTitlePan a::attr(title)').extract_first()
            bookmark_url = bookmark_block.css('.articleInfoPan p:first-child a::attr(href)').extract_first()
            bookmark_comment = bookmark_block.css('.thumbTBriefTxt p::text').extract_first()
            bookmark_tags = bookmark_block.css('.thumbTBriefTxt .tagName li a::text').extract()

            # convert date from unix integer in utc to an ISO-8601 date string
            bookmark_date = datetime.utcfromtimestamp(bookmark_date).isoformat()

            # determine whether this is a private link or not
            bookmark_private = len(bookmark_block.css('.privateArticle')) > 0

            # create an item
            yield Bookmark(delicious_id=bookmark_id, created=bookmark_date, title=bookmark_title,
                url=bookmark_url, comment=bookmark_comment, tags=bookmark_tags, private=bookmark_private)

            # if the item is not private _and_ we're asked to mark it private, do the thing
            if not bookmark_private and self.settings.get('DELICIOUS_MARK_PRIVATE'):
                yield scrapy.FormRequest(urlparse.urljoin(response.url, '/save/bookmark'),
                    callback=self.on_update_bookmark_response,
                    meta={'bookmark_id': bookmark_id},
                    formdata={
                        'replace': 'true',
                        'url': bookmark_url,
                        'description': bookmark_title,
                        'tags': ','.join(bookmark_tags),
                        'note': bookmark_comment or '',
                        'private': 'true'
                    },
                    # if this isn't present, 404
                    headers={'X-Requested-With': ['XMLHttpRequest']},
                )

        # after parsing all bookmarks, find the next page and go there
        next_link = response.css('.pagination a[aria-label=Next]::attr(href)').extract_first()

        if next_link:
            yield scrapy.Request(urlparse.urljoin(response.url, next_link),
                callback=self.on_bookmark_response)

    def on_update_bookmark_response(self, response):
        """
        Callback method triggered on response from /bookmark/save.
        """
        # extract bookmark id from response
        bookmark_id = response.meta.get('bookmark_id', '(unknown)')

        # log whether we succeeded or failed
        if response.status == 200:
            self.logger.info("Marked bookmark {} as private.".format(bookmark_id))
        else:
            self.logger.error("Unable to mark bookmark {} as private, due to code {}.".format(
                bookmark_id, response.status))
