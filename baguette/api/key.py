#-*- coding:utf-8 -*-
"""
Module managing all the keys calls to baguette.io
"""
import logging
import requests
import baguette.settings
import baguette.utils as utils

LOGGER = logging.getLogger(__name__)

def create(name, key):
    """
    Given a name/public key, try to create a key.
    :param name: The key to create.
    :type name: str
    :returns: The status of the creation.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'keys/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.post(url, data={'name':name, 'public': key}, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()

def find(limit, offset):
    """
    List the keys.
    :param limit: The number of keys per request.
    :type limit: int
    :param offset: The offset to start to retrieve the keys from.
    :type offset: int
    :returns: The status of the request.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'keys/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.get(url, params={'limit':limit, 'offset': offset}, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()

def delete(name):
    """
    Given a name, try to delete a key.
    :param name: The key to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'keys/{0}'.format(name)
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.delete(url, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, {}
