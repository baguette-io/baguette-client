#-*- coding:utf-8 -*-
"""
tests for the api module.
"""
# pylint:disable=no-member
# pylint:disable=wildcard-import,unused-wildcard-import

import baguette.api
from .fixtures import *

def test_set_token():
    """
    Check that set_token() write into a file.
    """
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        baguette.api.set_token('my_token')
    file_mock().write.assert_called_once_with('my_token')

def test_get_token():
    """
    Check that get_token() retrieve from the file.
    """
    with mock.patch('os.path.exists'):
        file_mock = mock.mock_open(read_data='my_token')
        with mock.patch('baguette.api.open', file_mock, create=True):
            baguette.api.set_token('my_token')
            assert baguette.api.get_token() == 'my_token'

def test_login_ok(req_ok):
    """
    Login API call which succeed.
    """
    req_ok({'token':'jwt'})
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        assert baguette.api.login('email', 'password')
    file_mock().write.assert_called_once_with('jwt')

def test_login_error(req_raise):
    """
    Login API call which failed.
    """
    req_raise()
    file_mock = mock.mock_open()
    with mock.patch('baguette.api.open', file_mock, create=True):
        assert not baguette.api.login('email', 'password')
    file_mock().write.assert_not_called()

def test_signup_ok(req_ok):
    """
    signup API call which succeed.
    """
    req_ok({'email':'email', 'username':'username'})
    status, infos = baguette.api.signup('email', 'username', 'password')
    assert status
    assert 'email' in infos
    assert 'username' in infos

def test_signup_error(req_raise):
    """
    signup API call which failed.
    """
    req_raise({})
    status, infos = baguette.api.signup('email', 'username', 'password')
    assert not status
    assert isinstance(infos, dict)

def test_create_app_ok(req_ok):
    """
    Create app API call which succeed.
    """

def test_create_app_error(req_raise):
    """
    Create app API call which failed.
    """
