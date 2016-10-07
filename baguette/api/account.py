#-*- coding:utf-8 -*-
"""
Module managing all the account calls to baguette.io
"""
import logging
import os
import requests
import baguette.settings

LOGGER = logging.getLogger(__name__)


def set_token(token):
    """
    Store the JWT in the user's home.
    :param token: the token to store.
    :type token: str
    :rtype: None
    """
    home = os.path.expanduser("~")
    with open(os.path.join(home, '.baguetterc'), 'w') as filename:
        filename.write(token)

def get_token():
    """
    Try to retrieve the JWT in the user's home.
    :returns: The token value.
    :rtype: None, str
    """
    home = os.path.expanduser("~")
    baguetterc = os.path.join(home, '.baguetterc')
    if not os.path.exists(baguetterc):
        return None
    return open(baguetterc).read().strip()

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
    return True, result.json()

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
    endpoint = 'accounts/login/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    result = requests.post(url, data={'email':email, 'password':password})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False
    set_token(result.json()['token'])
    return True
