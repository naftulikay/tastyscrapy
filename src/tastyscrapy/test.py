#!/usr/bin/env python3

from tastyscrapy.settings import is_mark_private
from unittest import mock

import unittest


class SettingsTest(unittest.TestCase):

    @mock.patch('tastyscrapy.settings.environ')
    def test_mark_private(self, mock_environ):
        """Test that the mark private setting properly reflects the environment variable."""
        # test empty
        mock_environ.get.return_value = False
        self.assertFalse(is_mark_private())
        # test truthy values
        mock_environ.get.return_value = 'true'
        self.assertTrue(is_mark_private())
        mock_environ.get.return_value = 'yes'
        self.assertTrue(is_mark_private())
        mock_environ.get.return_value = 'on'
        self.assertTrue(is_mark_private())
        # test unknown value
        mock_environ.get.return_value = 'dangus'
        self.assertFalse(is_mark_private())
