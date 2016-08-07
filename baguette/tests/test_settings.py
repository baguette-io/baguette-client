#-*- coding:utf-8 -*-
"""
tests for the settings module.
"""
# pylint:disable=no-member
# pylint:disable=wildcard-import,unused-wildcard-import

import baguette.settings
from .fixtures import *

def test_simple():
    """
    Dummy test that check that all
    the default options are present.
    """
    assert baguette.settings.default
    assert baguette.settings.default['api']
