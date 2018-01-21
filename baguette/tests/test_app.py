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

def test_create_with_token_ok(req_ok):
    """
    Try to create an app with a token.
    """
    req_ok({'repo_uri':'uri'})
    jwt = mock.Mock(return_value='my_token')
    with mock.patch('baguette.utils.get', jwt):
        assert baguette.api.app.create('xxx', 'default')

def test_create_error(req_raise):
    """
    Create app API call which failed.
    """
    req_raise({})
    res = mock.Mock(return_value='my_token')
    with mock.patch('baguette.utils.get', res):
        result, _ = baguette.api.app.create('xxx', 'default')
        assert not result

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

def test_list_ok(req_ok):
    """
    find API call which succeed.
    """
    req_ok({'count': 2, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'date_modified': '2016-10-07T18:24:32',
                                                       'name': 'un'},
                                                      {'date_created': '2016-10-09T01:19:57',
                                                       'date_modified': '2016-10-09T01:19:57',
                                                       'name': 'deux'},
                                                     ], 'next': None})
    status, infos = baguette.api.app.find(10, 0, 'default')
    assert status
    assert 'count' in infos
    assert 'results' in infos

def test_list_error(req_raise):
    """
    find API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.app.find(10, 0, 'default')
    assert not status
    assert 'detail' in infos

def test_delete_ok(req_ok):
    """
    delete API call which succeed.
    """
    req_ok({})
    status, infos = baguette.api.app.delete('my_app', 'default')
    assert status
    assert infos == {}

def test_delete_error(req_raise):
    """
    delete API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.app.delete('app', 'default')
    assert not status
    assert 'detail' in infos

def test_delete_remove_remote(req_ok, git_repo, tmpdir):
    """
    When deleting an app, delete the remote if the app name matches.
    """
    req_ok({})
    path = os.path.join(str(tmpdir), '.git', 'config')
    #Name doesn't match
    baguette.api.app.git_init('myapp.git')
    status, _ = baguette.api.app.delete('mywrongapp', 'default')
    assert status
    assert 'remote "baguette.io"' in open(path).read()
    #Name matches
    status, _ = baguette.api.app.delete('myapp', 'default')
    assert status
    assert 'remote "baguette.io"' not in open(path).read()
