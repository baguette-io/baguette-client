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

def create(name, vpc):
    """
    Given a name, try to create an app.
    Idempotent.
    :param name: The app to create.
    :type name: str
    :param vpc: The vpc name containing the app.
    :type vpc: str
    :returns: The status of the creation.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'projects/'
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.post(url, data={'name':name, 'vpc': vpc}, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    return True, result.json()

def already_in_baguette():
    """
    Check if the current git repo
    is already part of baguette.io.
    :param remote: The remote to check.
    :type remote: str
    :rtype: None
    """
    repo = git.Repo(os.getcwd())
    return any(r for r in repo.remotes if r.name == 'baguette.io')

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

def find(limit, offset):
    """
    List the apps.
    :param limit: The number of apps per request.
    :type limit: int
    :param offset: The offset to start to retrieve the apps from.
    :type offset: int
    :returns: The status of the request.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'projects/'
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
    Given a name, try to delete an app.
    :param name: The app to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: list (<bool>, <dict>)
    """
    #1. Check that we have a token.
    token = account.get_token()
    #2. Variables for the request.
    endpoint = 'projects/{0}'.format(name)
    url = baguette.settings.default['api'] + endpoint# pylint:disable=no-member
    headers = {'Authorization': 'JWT {0}'.format(token)}
    #3. Query.
    result = requests.delete(url, headers=headers)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as error:
        LOGGER.info(error)
        return False, result.json()
    #4. Cleanup the remote
    try:
        repo = git.Repo(os.getcwd())
    except git.exc.InvalidGitRepositoryError:
        pass
    else:
        url = '{0}.git'.format(name)
        if any(r for r in repo.remotes if r.name == 'baguette.io' and r.url.endswith(url)):
            repo.delete_remote('baguette.io')
    return True, {}
