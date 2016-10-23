#!/usr/bin/env python3

from os import environ


BOT_NAME = 'tastyscrapy'

# list all spider modules to run
SPIDER_MODULES = [
    'tastyscrapy.spiders',
]

# create new spiders in this module
NEWSPIDER_MODULE = 'tastyscrapy.spiders'

# pipelines
ITEM_PIPELINES = {
    'tastyscrapy.pipelines.DatabasePipeline': 500,
}

# pull in the username and password from environment variables
DELICIOUS_USERNAME = environ.get('DELICIOUS_USERNAME', '')
DELICIOUS_PASSWORD = environ.get('DELICIOUS_PASSWORD', '')


# allow batch private marking if the user wants it
def is_mark_private():
    return environ.get('DELICIOUS_MARK_PRIVATE', False) \
        in ['true', 'True', 'yes', 'on', True]

DELICIOUS_MARK_PRIVATE = is_mark_private()

# allow saving of database to custom output file
DATABASE_FILE = environ.get('DATABASE_FILE', 'delicious.db')
