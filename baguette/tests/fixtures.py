#-*- coding:utf-8 -*-
"""
Fixtures for the unit tests.
"""
import mock
import pytest
import requests
import baguette.settings

@pytest.fixture(autouse=True)
def settings():
    """
    Auto use this fixture for each test.
    """
    baguette.settings.load()

@pytest.fixture
def req_raise():
    """
    Fixture for requests to simulate a HTTP error.
    """
    res = requests.Response()
    res.status_code = 404
    requests.get = mock.Mock(return_value=res)
    requests.post = mock.Mock(return_value=res)

@pytest.fixture
def req_ok():
    """
    Requests factory.
    """
    res = mock.Mock()
    res.json = lambda: {'token':'jwt'}
    requests.get = mock.Mock(return_value=res)
    requests.post = mock.Mock(return_value=res)
