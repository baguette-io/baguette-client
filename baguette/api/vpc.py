#-*- coding:utf-8 -*-
"""
Module managing all the namespaces calls to baguette.io
"""
import logging
import requests
import baguette.settings
import baguette.utils as utils

LOGGER = logging.getLogger(__name__)

def create(name, organization):
    """
    Given a name, try to create a namespace.
    :param name: The namespace to create.
    :type name: str
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the creation.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'vpcs/{0}/'.format(organization)
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.post(url, json={'name':name}, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()

def find(limit, offset, organization):
    """
    List the namespaces.
    :param limit: The number of namespaces per request.
    :type limit: int
    :param offset: The offset to start to retrieve the namespaces from.
    :type offset: int
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'vpcs/{}/'.format(organization)
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

def delete(name, organization):
    """
    Given a name, try to delete a namespace.
    :param name: The namespace to delete.
    :type name: str
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the deletion.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'vpcs/{0}/{1}/'.format(organization, name)
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.delete(url, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if result.status_code == 403:
            result = {name: 'cannot be deleted'}
        elif result.status_code == 404:
            try:
                result = result.json()
            except:
                result = {name: 'not found'}
        else:
            result = result.json()
        LOGGER.info(error)
        return False, result
    return True, {}
