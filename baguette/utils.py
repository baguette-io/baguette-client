#-*-coding:utf-8 -*-
"""
Utils.
"""
import ConfigParser
import os

def set_config(username, token):
    """
    Store the username and JWT in the user's home.
    :param username: the username to store.
    :type username: str
    :param token: the token to store.
    :type token: str
    :rtype: None
    """
    home = os.path.expanduser("~")
    config = ConfigParser.RawConfigParser()
    config.set('DEFAULT', 'user', username)
    config.set('DEFAULT', 'token', token)
    with open(os.path.join(home, '.baguetterc'), 'w') as filename:
        config.write(filename)

def get(key):
    """
    Try to retrieve the key's value in baguette.rc
    :returns: The key value.
    :rtype: None, str
    """
    config = ConfigParser.ConfigParser()
    home = os.path.expanduser("~")
    baguetterc = os.path.join(home, '.baguetterc')
    if not os.path.exists(baguetterc):
        return None
    config.read(baguetterc)
    return config.get('DEFAULT', key).strip()
