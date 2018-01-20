#-*- coding:utf-8 -*-
"""
tests for the organization module.
"""
# pylint:disable=no-member
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name
# pylint:disable=wildcard-import,unused-wildcard-import
import baguette.api.organization
from .fixtures import *

def test_create_ok(req_ok):
    """
    create API call which succeed.
    """
    req_ok({'name':'my_orga', 'deletable': True,
            'date_created':'date_created', 'date_modified':'date_modified'})
    status, infos = baguette.api.organization.create('my_orga')
    assert status
    assert 'name' in infos
    assert 'deletable' in infos
    assert 'date_created' in infos
    assert 'date_modified' in infos

def test_create_error(req_raise):
    """
    create API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.organization.create('my_orga')
    assert not status
    assert 'detail' in infos

def test_list_ok(req_ok):
    """
    find API call which succeed.
    """
    req_ok({'count': 2, 'previous': None, 'results': [{'date_created': '2016-10-07T18:24:32',
                                                       'date_modified': '2016-10-07T18:24:32',
                                                       'name': 'default', 'deletable': False},
                                                      {'date_created': '2016-10-09T01:19:57',
                                                       'date_modified': '2016-10-09T01:19:57',
                                                       'name': 'deux', 'deletable': 'True'},
                                                     ], 'next': None})
    status, infos = baguette.api.organization.find(10, 0)
    assert status
    assert 'count' in infos
    assert 'results' in infos

def test_list_error(req_raise):
    """
    find API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.organization.find(10, 0)
    assert not status
    assert 'detail' in infos

def test_delete_ok(req_ok):
    """
    delete API call which succeed.
    """
    req_ok({})
    status, infos = baguette.api.organization.delete('my_orga')
    assert status
    assert infos == {}

def test_delete_error(req_raise):
    """
    delete API call which fails.
    """
    req_raise(result={'detail': 'Signature has expired.'})
    status, infos = baguette.api.organization.delete('my_orga')
    assert not status
    assert 'detail' in infos

def test_delete_non_deletable(req_raise):
    """
    delete API call which succeed.
    """
    req_raise(result={'detail':'You do not have permission to perform this action.'})
    status, infos = baguette.api.organization.delete('my_orga-default')
    assert not status
    assert 'detail' in infos
