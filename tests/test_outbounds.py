#!/bin/python3

# SPDX-FileCopyrightText: 2021 Jens Erdmann
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import json
import unittest

TEST_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add to PYTHON_PATH
sys.path.insert(0, TEST_DIR)

from flict.flictlib import flict_config
from flict.impl import FlictImpl


class ArgsMock:
    def __init__(self, license_expression, no_relicense=False, relicense_file=flict_config.DEFAULT_RELICENSE_FILE):
        self.output_format = 'JSON'
        self.license_group_file = flict_config.DEFAULT_GROUP_FILE 
        self.translations_file = flict_config.DEFAULT_TRANSLATIONS_FILE
        self.relicense_file = relicense_file
        self.matrix_file = flict_config.DEFAULT_MATRIX_FILE
        self.scancode_file = None
        self.extended_licenses = False
        self.license_expression = license_expression
        self.no_relicense = no_relicense

class OutboundTest(unittest.TestCase):

    def _test_expression(self, expression, result):
        args = ArgsMock(expression)
        ret = FlictImpl(args).suggest_outbound_candidate()
        self.assertEqual(json.loads(ret), result)


    def test_outbound(self):
        self._test_expression(['MIT'], ['MIT'])
        self._test_expression(['MIT and MIT'], ['MIT'])
        self._test_expression(['MIT and MIT and BSD-3-Clause'], ['BSD-3-Clause', 'MIT'])
        self._test_expression(['GPL-2.0-only and (MIT or BSD-3-Clause)'], ['GPL-2.0-only'])
        self._test_expression(['GPL-2.0-only or (MIT and BSD-3-Clause)'], ['BSD-3-Clause', 'GPL-2.0-only', 'MIT'])
        self._test_expression(['GPL-2.0-only and (Apache-2.0 or MIT)'], ['GPL-2.0-only'])
        self._test_expression(['GPL-2.0-only or (Apache-2.0 and MIT)'], ['Apache-2.0', 'GPL-2.0-only', 'MIT'])
        self._test_expression(['GPL-2.0-only and Apache-2.0'], [])
        self._test_expression(['GPL-2.0-only and Apache-2.0 and MPL-2.0'], [])
        self._test_expression(['GPL-2.0-only and MPL-2.0'], ['GPL-2.0-only', 'GPL-2.0-or-later'])
        self._test_expression(['GPL-2.0-only and MPL-2.0'], ['GPL-2.0-only', 'GPL-2.0-or-later'])
        self._test_expression(['GPL-2.0-only and (MPL-2.0 or Apache-2.0) and BSD-3-Clause'],
                              ['GPL-2.0-only', 'GPL-2.0-or-later'])
        self._test_expression(['(GPL-2.0-only or MPL-2.0) and (Apache-2.0 or BSD-3-Clause)'],
                              ['AGPL-3.0-or-later', 'GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-or-later', 'LGPL-2.1-or-later'])

    def test_no_relicense(self):
        # args = ArgsMock(['GPL-2.0-only and MPL-2.0'], no_relicense=True)
        # ret = FlictImpl(args).suggest_outbound_candidate()
        # self.assertEqual(json.loads(ret), ['GPL-2.0-only'])

        args = ArgsMock(['GPL-2.0-only and MPL-2.0'], relicense_file='')
        ret = FlictImpl(args).suggest_outbound_candidate()
        self.assertEqual(json.loads(ret), ['GPL-2.0-only'])


if __name__ == '__main__':
    unittest.main()