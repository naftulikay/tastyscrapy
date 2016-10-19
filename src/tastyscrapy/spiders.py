#!/usr/bin/env python3

from datetime import datetime
from tastyscrapy.exceptions import LoginFailedException
from tastyscrapy.items import LoginSuccess

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
        if response.status != 200:
            raise LoginFailedException("Received response {} when trying to log in.".format(response.status))

        # create variable for storing the json payload
        payload = None

        try:
            payload = json.loads(response.text)
        except:
            raise LoginFailedException("Unable to parse JSON response.")

        if xjpath.path_lookup(payload, 'status') != ('success', True):
            raise LoginFailedException("Unable to log in using provided credentials.")

        # emit an item which shows that we logged in successfully for audit tracking
        yield LoginSuccess(created=datetime.utcnow().isoformat())

        redirect, is_success = xjpath.path_lookup(payload, 'redirect')

        # start parsing items
        yield scrapy.Request(redirect if is_success else "https://del.icio.us/{}".format(
            self.settings.get('DELICIOUS_USERNAME')), callback=self.on_bookmark_response)

    def on_bookmark_response(self, response):
        """
        Callback method triggered when login has succeeded or the next
        bookmark page has been fetched.
        """
        pass
