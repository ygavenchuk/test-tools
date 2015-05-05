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

from sys import version_info
from os.path import join as path_join, abspath, dirname
from json import load as json_load
from copy import deepcopy
from inspect import stack as inspect_stack


__author__ = 'y.gavenchuk aka murminathor'
__all__ = ['FixtureManager', ]

if version_info[0] == 2:
    from codecs import open


class FixtureManager(object):
    @staticmethod
    def _get_caller_filename():
        """
        Find and return filename of outer caller (external script)

        :return str:
        """
        # if extension of file's name in __file__ is '.pyc' or '.pyo' then next
        # file will be with the same name but with extension '.py'!!!
        # So, we need to use generalized extension of file
        file_name = __file__[:-1] if __file__[-1] in set('oc') else __file__

        for item in inspect_stack():
            if item and file_name not in item:
                return item[1]

        return __file__

    def __init__(self):
        self.fixture_data = {}

    def load(self, fixture_data=None, fixture_file=None, file_ext='json',
             current_file=None):
        """
            Load fixtures from iterable (list, dict, tuple, ...) instance
            (fixture_data) or file

            :param Iterable fixture_data: iterable data container
            :param str|unicode fixture_file: name of file, from where will be
                data loaded .
            :param str|unicode file_ext: extension of file without(!) leading
                dot. If empty string or None - no additional extensions used
            :param current_file: string - file, indicates from where need to
                search relative path of fixture_file

            :raise ImportError: - if fixture data source is undefined
        """
        if fixture_data is not None:
            self.fixture_data = fixture_data
        elif fixture_file is not None:
            if file_ext:
                fixture_file += '.' + file_ext

            fixture_path = self.get_fixture_path(fixture_file, current_file)
            with open(fixture_path, 'r', encoding='utf-8') as fp:
                self.fixture_data = json_load(fp)
        else:
            raise ImportError('Undefined fixture data source')

    def get(self, fixture_name):
        """
            Get fixture data by it's name.

            :param str|unicode fixture_name: name of fixture, which data need
                to return
            :return Iterable: if fixture_name doesn't exists - will be
                returned an empty dict
        """
        if fixture_name in self.fixture_data:
            result = self.fixture_data[fixture_name]
        else:
            result = {}

        return deepcopy(result)

    def __getitem__(self, item):
        return self.get(item)

    @classmethod
    def get_fixture_path(cls, fixture_file, current_file=None):
        """
            Build and return absolute path to the fixture's file.

            :note: method doesn't check existence of file

            :param str|unicode fixture_file: name of file, from where will be
                loaded data.
            :param str|unicode|None current_file: file, indicates from where
                need to search relative path of fixture_file

            :return str|unicode:
        """

        if not current_file:
            current_file = cls._get_caller_filename()

        return path_join(
            abspath(dirname(current_file)), 'fixtures', fixture_file
        )
