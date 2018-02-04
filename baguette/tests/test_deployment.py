#-*- coding:utf-8 -*-
"""
tests for the deployment module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import baguette.api.deployment
from .fixtures import *

def test_list_ok(req_ok):
    """
    find API call which succeed.
    """
    req_ok({'count': 2, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'name': 'default', 'fail': False},
                                                      {'date_created': '2016-10-09T01:19:57',
                                                       'name': 'deux', 'fail': 'True'},
                                                     ], 'next': None})
    status, infos = baguette.api.deployment.find(10, 0, 'default')
    assert status
    assert 'count' in infos
    assert 'results' in infos

def test_list_error(req_raise):
    """
    find API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.deployment.find(10, 0, 'default')
    assert not status
    assert 'detail' in infos

def test_detail_ok(req_ok):
    """
    detail API call which succeed.
    """
    req_ok({'count': 2, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'name': 'default', 'fail': False},
                                                      {'date_created': '2016-10-09T01:19:57',
                                                       'name': 'deux', 'fail': 'True'},
                                                     ], 'next': None})
    status, infos = baguette.api.deployment.detail('test', 'default')
    assert status
    assert 'count' in infos
    assert 'results' in infos

def test_list_error(req_raise):
    """
    find API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.deployment.detail('test', 'default')
    assert not status
    assert 'detail' in infos

def test_stop_ok(req_ok):
    """
    stop API call which succeed.
    """
    req_ok({})
    status, infos = baguette.api.deployment.stop('uid', 'orga')
    assert status
    assert infos == {}

def test_stop_error(req_raise):
    """
    stop API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.deployment.stop('uid', 'orga')
    assert not status
    assert 'detail' in infos
