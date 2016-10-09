#-*- coding:utf-8 -*-
"""
Fixtures for the unit tests.
"""
import git
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
    def factory(result=None, code=404):
        """
        Factory.
        """
        res = requests.Response()
        res.status_code = code
        res.json = lambda: result
        requests.get = mock.Mock(return_value=res)
        requests.post = mock.Mock(return_value=res)
        requests.delete = mock.Mock(return_value=res)
    return factory

@pytest.fixture
def req_ok():
    """
    Fixture for requests to simulate a successfull HTTP request.
    """
    def factory(result):
        """
        Factory.
        """
        res = mock.Mock()
        res.json = lambda: result
        requests.get = mock.Mock(return_value=res)
        requests.post = mock.Mock(return_value=res)
        requests.delete = mock.Mock(return_value=res)
    return factory


@pytest.yield_fixture()
def git_repo(tmpdir):
    """
    Patch os.getcwd() and initialize a git repo.
    """
    repo = mock.Mock(return_value=str(tmpdir))
    with mock.patch('os.getcwd', repo):
        git.Repo.init(str(tmpdir))
        yield
