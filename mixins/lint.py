#!/usr/bin/env python3
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

"""Lint the index.yaml file as well as all files ending with .mixin.

Taken from https://github.com/colcon/colcon-mixin-repository.
Modified for the AWS mixins repository.
"""
__author__ = 'Dirk Thomas'
__license__ = 'CC0 1.0 Universal'
__maintainer__ = 'Dirk Thomas'

import logging
import os
import sys


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    from yamllint.cli import run
except ImportError:
    logger.exception("Failed to import Python package 'yamllint'")
    sys.exit(0)

any_error = False
for name in sorted(os.listdir()):
    if name != 'index.yaml' and not name.endswith('.mixin'):
        continue

    try:
        run([
            '--config-data',
            '{'
            'extends: default, '
            'rules: {'
            'document-start: {present: false}, '
            'empty-lines: {max: 0}, '
            'key-ordering: {}, '
            'line-length: {max: 999}'
            '}'
            '}',
            '--strict',
            name,
        ])
        logger.info('Linting complete.')
    except SystemExit as e:
        any_error |= bool(e.code)
        continue
    assert False, 'run() should always raise SystemExit'

sys.exit(1 if any_error else 0)
