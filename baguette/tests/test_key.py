#-*- coding:utf-8 -*-
"""
tests for the key module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import baguette.api.key
from .fixtures import *

def test_create_ok(req_ok):
    """
    create API call which succeed.
    """
    req_ok({'name':'my_key', 'public':'public', 'fingerprint':'fingerprint',
            'date_created':'date_created', 'date_modified':'date_modified'})
    status, infos = baguette.api.key.create('my_key', 'public')
    assert status
    assert 'name' in infos
    assert 'public' in infos
    assert 'fingerprint' in infos
    assert 'date_created' in infos
    assert 'date_modified' in infos

def test_create_error(req_raise):
    """
    create API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.key.create('my_key', 'public')
    assert not status
    assert 'detail' in infos

def test_list_ok(req_ok):
    """
    find API call which succeed.
    """
    req_ok({'count': 3, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'date_modified': '2016-10-07T18:24:32',
                                                       'fingerprint': 'fingerprint',
                                                       'name': 'un', 'public': 'ssh-rsa1'},
                                                      {'date_created': '2016-10-09T01:19:57',
                                                       'date_modified': '2016-10-09T01:19:57',
                                                       'fingerprint': 'fingerprint',
                                                       'name': 'deux', 'public': 'ssh-rsa2'},
                                                      {'date_created': '2016-10-09T01:20:10',
                                                       'date_modified': '2016-10-09T01:20:10',
                                                       'fingerprint': 'fingerprint',
                                                       'name': 'trois', 'public': 'ssh-rsa3'},
                                                     ], 'next': None})
    status, infos = baguette.api.key.find(10, 0)
    assert status
    assert 'count' in infos
    assert 'results' in infos

def test_list_error(req_raise):
    """
    find API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.key.find(10, 0)
    assert not status
    assert 'detail' in infos

def test_delete_ok(req_ok):
    """
    delete API call which succeed.
    """
    req_ok({})
    status, infos = baguette.api.key.delete('my_key')
    assert status
    assert infos == {}

def test_delete_error(req_raise):
    """
    delete API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.key.delete('my_key')
    assert not status
    assert 'detail' in infos
