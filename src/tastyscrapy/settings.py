#!/usr/bin/env python3

from os import environ


BOT_NAME = 'tastyscrapy'

# list all spider modules to run
SPIDER_MODULES = [
    'tastyscrapy.spiders',
]

# create new spiders in this module
NEWSPIDER_MODULE = 'tastyscrapy.spiders'

# pull in the username and password from environment variables
DELICIOUS_USERNAME = environ.get('DELICIOUS_USERNAME', '')
DELICIOUS_PASSWORD = environ.get('DELICIOUS_PASSWORD', '')
