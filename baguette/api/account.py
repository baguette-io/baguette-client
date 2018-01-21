#-*- coding:utf-8 -*-
"""
Module managing all the account calls to baguette.io
"""
import logging
import os
import stat
import requests
import baguette.settings
import baguette.utils as utils

LOGGER = logging.getLogger(__name__)

def create_default_key(username, key):
    """
    Create the default key when signup.
    :param username: The username creating the account.
    :type username: str
    :param key: Contains all the key informations.
    :type key:dict
    :rtype: None
    """
    home = os.path.expanduser("~")
    directory = os.path.join(home, '.ssh')
    public = os.path.join(directory, 'baguetteio-{0}-default.pub'.format(username))
    private = os.path.join(directory, 'baguetteio-{0}-default.pem'.format(username))
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.chmod(directory, stat.S_IREAD)
    open(public, 'w').write(key['public'])
    os.chmod(public, stat.S_IREAD)
    open(private, 'w').write(key['private'])
    os.chmod(private, stat.S_IREAD)

def signup(email, username, password):
    """
    Create an account on baguette.io
    :param email: The email to signup with.
    :type email: str
    :param username: The username to signup in with.
    :type username: str
    :param password: The password to signup in with.
    :type password: str
    :returns: The status of the signup.
    :rtype: tuple (bool, dict)
    """
    #1. Prepare the URL
    endpoint = 'accounts/register/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    #2. Query
    result = requests.post(url, {'username': username, 'email': email, 'password': password,
                                 'confirm_password':password})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    result = result.json()
    #3. Create the default key
    create_default_key(result['account']['username'], result['key'])
    return True, result

def login(username, password):
    """
    Given credentials, try to login baguette.io.
    :param username: The username to authenticate.
    :type username: str
    :param password: The account password.
    :type password: str
    :returns: The status of the login.
    :rtype: bool
    """
    endpoint = 'accounts/login/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    result = requests.post(url, json={'username':username, 'password':password})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False
    utils.set_config(username, result.json()['token'])
    return True

def quotas():
    """
    List all the account quotas.
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Check that we have a token.
    token = utils.get('token')
    #2. Variables for the request.
    endpoint = 'quotas/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.get(url, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()
