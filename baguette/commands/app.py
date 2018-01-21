#-*-coding:utf-8 -*-
"""
App commands.
"""
import os
import click
import git
import baguette.api.app as api
import baguette.utils as utils
from .utils import display_errors

@click.group()
def app():
    """
    App group commands.
    """

@click.option('--organization', default=None, type=str, help='The namespace organization.')
@click.argument('name', required=False)
@app.command(name='app-create', help='Create an app of the current git repo.')
def create(name, organization):
    """
    Create an app of the current git repo.
    :param name: The app name. Optional.
    :type name: None, str
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the creation.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
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
    created, infos = api.create(name, organization)
    if created:
        api.git_init(infos['uri'])
        click.echo("""{0}: {1} created.
baguette.io` remote added.
When pushing to this remote, your app will be automatically deployed.""".format(organization, name))
        return True
    return display_errors(infos)

@click.option('--offset', default=0, type=int, help='The offset to start retrieving the apps from.')
@click.option('--limit', default=10, type=int, help='The number of apps per request.')
@click.option('--organization', default=None, type=str, help='The namespace organization.')
@app.command(name='app-list', help='List all the apps.')
def find(offset, limit, organization):
    """
    List all the apps.
    :param limit: The number of apps per request.
    :type limit: int
    :param offset: The offset to start to retrieve the apps from.
    :type offset: int
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
    #1. Call the API to get all the apps
    status, infos = api.find(limit, offset, organization)
    if status:
        click.echo('\n{0} : starting {1}, listing {2} apps on a total of {3} apps.\n'.format(
            organization,
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Name\tURI\tCreation Date\n')
        for result in infos['results']:
            click.echo('{0}\t{1}\t{2}'.format(
                result['name'],
                result['uri'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)

@click.option('--organization', default=None, type=str, help='The namespace organization.')
@click.argument('name')
@app.command(name='app-delete', help='Delete an app.')
def delete(name, organization):
    """
    Delete an app.
    :param name: The app name to delete.
    :type name: None, str
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the deletion.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
    #1. Call the API to delete the key
    deleted, infos = api.delete(name, organization)
    if deleted:
        click.echo('{0} : app {1} deleted.'.format(organization, name))
        return True
    return display_errors(infos)
