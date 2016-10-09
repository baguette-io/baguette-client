#-*- coding:utf-8 -*-
"""
Module managing all the app calls to baguette.io
"""
import logging
import os
import git
import requests
import baguette.settings
import baguette.api.account as account

LOGGER = logging.getLogger(__name__)

def create(name):
    """
    Given a name, try to create an app.
    Idempotent.
    :param name: The app to create.
    :type name: str
    :returns: The status of the creation.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    if not token:
        return False
    #2. Variables for the request.
    endpoint = 'projects/'
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

def git_init(remote):
    """
    Add the baguette.io remote
    to the current git repo, if not present.
    :param remote: The remote to add.
    :type remote: str
    :rtype: None
    """
    repo = git.Repo(os.getcwd())
    if not any(r for r in repo.remotes if r.name == 'baguette.io'):
        repo.create_remote('baguette.io', remote)
