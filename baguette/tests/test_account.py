#-*- coding:utf-8 -*-
"""
tests for the account module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import baguette.api.account
from .fixtures import *

def test_login_ok(req_ok):
    """
    Login API call which succeed.
    """
    req_ok({'token':'jwt'})
    file_mock = mock.mock_open()
    with mock.patch('baguette.utils.open', file_mock, create=True):
        assert baguette.api.account.login('username', 'password')
    file_mock().write.assert_has_calls([mock.call('[DEFAULT]\n'), mock.call('user = username\n'), mock.call('token = jwt\n'), mock.call('\n')])

def test_login_error(req_raise):
    """
    Login API call which failed.
    """
    req_raise()
    file_mock = mock.mock_open()
    with mock.patch('baguette.utils.open', file_mock, create=True):
        assert not baguette.api.account.login('username', 'password')
    file_mock().write.assert_not_called()

def test_signup_ok(req_ok):
    """
    signup API call which succeed.
    """
    file_mock = mock.mock_open()
    req_ok({'account':{'email': 'email', 'username':'username'},
            'key':{'name':'default', 'private':'', 'public':'', 'fingerprint':''}})
    with mock.patch('baguette.utils.open', file_mock, create=True),\
            mock.patch('os.chmod'), mock.patch('os.makedirs'):
        status, infos = baguette.api.account.signup('email', 'username', 'password')
    assert status
    assert 'account' in infos
    assert 'email' in infos['account']
    assert 'username' in infos['account']
    assert 'key' in infos
    assert 'name' in infos['key']
    assert 'private' in infos['key']
    assert 'public' in infos['key']
    assert 'fingerprint' in infos['key']

def test_signup_error(req_raise):
    """
    signup API call which failed.
    """
    req_raise({})
    status, infos = baguette.api.account.signup('email', 'username', 'password')
    assert not status
    assert isinstance(infos, dict)


def test_create_default_key(req_ok):
    """
    When signup check that the key is written.
    """
    file_mock = mock.mock_open()
    req_ok({'account':{'email': 'email', 'username':'username'},
            'key':{'name':'default', 'private':'', 'public':'', 'fingerprint':''}})
    with mock.patch('baguette.api.account.open', file_mock, create=True),\
            mock.patch('os.chmod'), mock.patch('os.makedirs'):
        baguette.api.account.signup('email', 'username', 'password')
    assert file_mock().write.call_count == 2

def test_quotas(req_ok):
    """
    Quotas API call which succeed.
    """
    req_ok({'count': 3, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'key': 'max_projects', 'value':'1000.0000'},
                                                      {'date_created': '2016-10-07T18:24:32',
                                                       'key': 'max_vpcs', 'value':'1000.0000'},
                                                      {'date_created': '2016-10-07T18:24:32',
                                                       'key': 'max_jeys', 'value':'1000.0000'},
                                                     ], 'next': None})
    status, infos = baguette.api.account.quotas()
    assert status
    assert 'count' in infos
    assert 'results' in infos
