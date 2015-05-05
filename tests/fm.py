# -*- coding: utf-8 -*-
from unittest import TestCase

from test_tools.fixtureman import FixtureManager

__author__ = 'y.gavenchuk aka murminathor'
__all__ = ('FixtureManagerTestCase', )


class FixtureManagerTestCase(TestCase):
    def test_load_fixture_file(self):
        fm = FixtureManager()
        fm.load(fixture_file="fx_data")
        self.assertTrue(fm["test_data"])
        self.assertEqual(fm["test_data"], [[u'a', u'b']])
