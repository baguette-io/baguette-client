#-*- coding:utf-8 -*-
"""
Module managing all the API calls to baguette.io
"""
import logging
import os
import requests
import baguette.settings

LOGGER = logging.getLogger(__name__)

def store_token(token):
    """
    Store the JWT in the user's home.
    :param token: the token to store.
    :type token: str
    :rtype: None
    """
    home = os.path.expanduser("~")
    with open(os.path.join(home, '.baguetterc'), 'w') as filename:
        filename.write(token)

def login(email, password):
    """
    Given credentials, try to login baguette.io.
    :param email: The email to authenticate.
    :type email: str
    :param password: The account password.
    :type password: str
    :returns: The status of the login.
    :rtype: bool
    """
    endpoint = 'account/login/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    result = requests.post(url, data={'email':email, 'password':password})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False
    store_token(result.json()['token'])
    return True
