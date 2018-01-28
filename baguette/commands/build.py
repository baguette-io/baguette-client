#-*-coding:utf-8 -*-
"""
builds commands.
"""
import json
import click
import baguette.api.build as api
import baguette.utils as utils
from .utils import display_errors

@click.group()
def build():
    """
    Build group commands.
    """
@click.option('--offset', default=0, type=int, help='The offset to start retrieving the build from.')
@click.option('--limit', default=10, type=int, help='The number of builds per request.')
@click.option('--organization', default=None, type=str, help='The organization to fetch the builds.')
@build.command(name='build-list', help='List all the builds.')
def find(offset, limit, organization):
    """
    List all the builds.
    :param limit: The number of builds per request.
    :type limit: int
    :param offset: The offset to start to retrieve the builds from.
    :type offset: int
    :param organization: The build's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
    #1. Call the API to get all the builds
    status, infos = api.find(limit, offset, organization)
    if status:
        click.echo('\n{0} : starting {1}, listing {2} builds on a total of {3} builds.\n'.format(
            organization,
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Project\nUid\tStep\tFail\tCreation Date\n')
        for result in infos['results']:
            result = json.loads(result)
            click.echo('{0}\t{1}\t{2}\t{3}\t{4}'.format(
                result['repo'],
                result['uid'],
                result['step'],
                result['fail'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)
