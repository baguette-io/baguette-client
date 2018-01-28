#-*- coding:utf-8 -*-
"""
Module managing all the deployments calls to baguette.io
"""
import logging
import requests
import baguette.settings
import baguette.utils as utils

LOGGER = logging.getLogger(__name__)

def find(limit, offset, organization):
    """
    List the deployments.
    :param limit: The number of deployments per request.
    :type limit: int
    :param offset: The offset to start to retrieve the deployments from.
    :type offset: int
    :param organization: The deployment's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'deployments/{}/'.format(organization)
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
