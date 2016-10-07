#-*- coding:utf-8 -*-
"""
tests for the app module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import os
import baguette.api.app
from .fixtures import *

def test_create_app_with_token_ok(req_ok):
    """
    Try to create an app with a token.
    """
    req_ok({'repo_uri':'uri'})
    jwt = mock.Mock(return_value='my_token')
    with mock.patch('baguette.api.account.get_token', jwt):
        assert baguette.api.app.create('xxx')

def test_create_app_no_token_error(req_ok):
    """
    Try to create an app without token.
    """
    req_ok({'repo_uri':'uri'})
    res = mock.Mock(return_value=None)
    with mock.patch('baguette.api.account.get_token', res):
        assert not baguette.api.app.create('xxx')

def test_create_app_error(req_raise):
    """
    Create app API call which failed.
    """
    req_raise({})
    res = mock.Mock(return_value='my_token')
    with mock.patch('baguette.api.account.get_token', res):
        assert not baguette.api.app.create('xxx')

def test_git_init_ok(git_repo, tmpdir):
    """
    Add a remote to a current git directory.
    """
    path = os.path.join(str(tmpdir), '.git', 'config')
    assert 'remote "baguette.io"' not in open(path).read()
    baguette.api.app.git_init('baguette.io')
    assert 'remote "baguette.io"' in open(path).read()


def test_git_init_idempotent_ok(git_repo, tmpdir):
    """
    Don't add twice the remote to the current git directory.
    """
    path = os.path.join(str(tmpdir), '.git', 'config')
    baguette.api.app.git_init('baguette.io')
    baguette.api.app.git_init('baguette.io')
    assert open(path).read().count('remote "baguette.io"') == 1
