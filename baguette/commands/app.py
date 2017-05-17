#-*-coding:utf-8 -*-
"""
App commands.
"""
import os
import click
import git
import baguette.api.app as api
from .utils import display_errors

@click.group()
def app():
    """
    App group commands.
    """

@click.argument('name', required=False)
@app.command(name='app-create', help='Create an app of the current git repo.')
def create(name):
    """
    Create an app of the current git repo.
    :param name: The app name. Optional.
    :type name: None, str
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Check that we are currently in a git repo.
    try:
        git.Repo(os.getcwd())
    except git.exc.InvalidGitRepositoryError:
        click.echo('The current path is not the root of the repository.')
        return False
    #2. Check that the current git repo is not already in baguette.io
    if api.already_in_baguette():
        click.echo('The current repository has already a baguette.io \'s remote.')
        return False
    #3. Generate the name if not set
    name = name or os.path.basename(os.getcwd())
    #4. Call the API to create the app
    created, infos = api.create(name)
    if created:
        api.git_init(infos['uri'])
        click.echo("""{0} created.
baguette.io` remote added.
When pushing to this remote, your app will be automatically deployed.""".format(name))
        return True
    return display_errors(infos)

@click.option('--offset', default=0, type=int, help='The offset to start retrieving the apps from.')
@click.option('--limit', default=10, type=int, help='The number of apps per request.')
@app.command(name='app-list', help='List all the apps.')
def find(offset, limit):
    """
    List all the apps.
    :param limit: The number of apps per request.
    :type limit: int
    :param offset: The offset to start to retrieve the apps from.
    :type offset: int
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the apps
    status, infos = api.find(limit, offset)
    if status:
        click.echo('Starting {0}, listing {1} apps on a total of {2} apps.'.format(
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Name\tURI\tCreation Date\n')
        for result in infos['results']:
            click.echo('{0}\t{1}\t{2}\t{3}'.format(
                result['name'],
                result['uri'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)

@click.argument('name')
@app.command(name='app-delete', help='Delete an app.')
def delete(name):
    """
    Delete an app.
    :param name: The app name to delete.
    :type name: None, str
    :returns: The status of the deletion.
    :rtype: bool
    """
    #1. Call the API to delete the key
    deleted, infos = api.delete(name)
    if deleted:
        click.echo('App {0} deleted.'.format(name))
        return True
    return display_errors(infos)
