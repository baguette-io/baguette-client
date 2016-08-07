#-*- coding:utf-8 -*-
"""
tests for the api module.
"""
# pylint:disable=no-member
# pylint:disable=wildcard-import,unused-wildcard-import

import baguette.api
from .fixtures import *

def test_store_token():
    """
    Check that store_token() write into a file.
    """
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        baguette.api.store_token('my_token')
    file_mock().write.assert_called_once_with('my_token')

def test_login_ok(req_ok):
    """
    Login API call which succeed.
    """
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        assert baguette.api.login('email', 'password')
    file_mock().write.assert_called_once_with('jwt')

def test_login_error(req_raise):
    """
    Login API call which failed.
    """
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        assert not baguette.api.login('email', 'password')
    file_mock().write.assert_not_called()
