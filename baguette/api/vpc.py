#-*- coding:utf-8 -*-
"""
Module managing all the vpcs calls to baguette.io
"""
import logging
import requests
import baguette.settings
import baguette.api.account as account

LOGGER = logging.getLogger(__name__)

def create(name):
    """
    Given a name, try to create a vpc.
    :param name: The vpc to create.
    :type name: str
    :returns: The status of the creation.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'vpcs/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.post(url, data={'name':name}, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()

def find(limit, offset):
    """
    List the vpcs.
    :param limit: The number of vpcs per request.
    :type limit: int
    :param offset: The offset to start to retrieve the vpcs from.
    :type offset: int
    :returns: The status of the request.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'vpcs/'
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
    Given a name, try to delete a vpc.
    :param name: The vpc to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'vpcs/{0}'.format(name)
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
