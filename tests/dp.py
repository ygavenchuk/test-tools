# -*- coding: utf-8 -*-
#
# Copyright 2015 Yuriy Gavenchuk aka murminathor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import TestCase
try:
    from unittest.mock import MagicMock
except ImportError:     # python2 and mock package
    from mock import MagicMock

from test_tools import data_provider

__author__ = 'y.gavenchuk aka murminathor'
__all__ = ['DataProviderTestCase', ]


class DataProviderTestCase(TestCase):
    def test_should_return_decorator(self):
        decorator = data_provider([])
        x = decorator(MagicMock())
        self.assertTrue(callable(decorator))
        self.assertTrue(callable(x))

    def test_empty_list_raises_type_error(self):
        decorator = data_provider([])
        x = decorator(MagicMock())
        self.assertRaises(TypeError, x)

    def test_non_iterable_data_raises_type_error(self):
        decorator = data_provider(1)
        x = decorator(MagicMock())
        self.assertRaises(TypeError, x)

    def test_method_calls_with_each_data_in_source_data_set(self):
        data_set = [
            [0],
            [self],
            [1, "bla, blah"],
            [7, 5.5, 8],
        ]
        dummy_self = MagicMock()
        orj_method = MagicMock()
        decorator = data_provider(data_set)
        x = decorator(orj_method)
        x(dummy_self)
        call_args_list = [list(y[0]) for y in orj_method.call_args_list]
        data_set_prepared = [[dummy_self] + y for y in data_set]

        self.assertEqual(data_set_prepared, call_args_list)

    def test_method_teardown_calls_for_each_item_in_source_data_set(self):
        data_set = [
            [0],
            [self],
            [1, "bla, blah"],
            [7, 5.5, 8],
        ]
        dummy_self = MagicMock()
        orj_method = MagicMock()
        decorator = data_provider(data_set)
        x = decorator(orj_method)
        x(dummy_self)
        self.assertEqual(dummy_self.tearDown.call_count, len(data_set) - 1)

    def test_method_setup_calls_for_each_item_in_source_data_set(self):
        data_set = [
            [0],
            [self],
            [1, "bla, blah"],
            [7, 5.5, 8],
        ]
        dummy_self = MagicMock()
        orj_method = MagicMock()
        decorator = data_provider(data_set)
        x = decorator(orj_method)
        x(dummy_self)
        self.assertEqual(dummy_self.setUp.call_count, len(data_set) - 1)
