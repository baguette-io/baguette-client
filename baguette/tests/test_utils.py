#-*- coding:utf-8 -*-
"""
tests for the utils module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import baguette.utils
from .fixtures import *

def test_set_config():
    """
    Check that set_config() write into a file.
    """
    file_mock = mock.mock_open()
    with mock.patch('baguette.utils.open', file_mock, create=True):
        baguette.utils.set_config('toto', 'titi')
    file_mock().write.assert_has_calls([mock.call('[DEFAULT]\n'), mock.call('user = toto\n'), mock.call('token = titi\n'), mock.call('\n')])

def test_get():
    """
    Check that get() retrieve from the file.
    """
    with mock.patch('os.path.exists'):
        with mock.patch('baguette.utils.configparser.ConfigParser.get', mock.Mock(return_value='my_user')):
            assert baguette.utils.get('user') == 'my_user'
        with mock.patch('baguette.utils.configparser.ConfigParser.get', mock.Mock(return_value='my_token')):
            assert baguette.utils.get('token') == 'my_token'
