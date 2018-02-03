#-*-coding:utf-8 -*-
"""
deployments commands.
"""
import json
import click
import baguette.api.deployment as api
import baguette.utils as utils
from .utils import display_errors

@click.group()
def deployment():
    """
    Build group commands.
    """
@click.option('--offset', default=0, type=int, help='The offset to start retrieving the deployment from.')
@click.option('--limit', default=10, type=int, help='The number of deployments per request.')
@click.option('--organization', default=None, type=str, help='The organization to fetch the deployments.')
@deployment.command(name='deployment-list', help='List all the deployments.')
def find(offset, limit, organization):
    """
    List all the deployments.
    :param limit: The number of deployments per request.
    :type limit: int
    :param offset: The offset to start to retrieve the deployments from.
    :type offset: int
    :param organization: The deployment's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
    #1. Call the API to get all the deployments
    status, infos = api.find(limit, offset, organization)
    if status:
        click.echo('\n{0} : starting {1}, listing {2} deployments on a total of {3} deployments.\n'.format(
            organization,
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Name\tUid\tStatus\tCreation Date\n')
        for result in infos['results']:
            result = json.loads(result)
            click.echo('{0}\t{1}\t{2}\t{3}'.format(
                result['name'],
                result['uid'],
                result['status'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)

@click.argument('uid')
@click.option('--organization', default=None, type=str, help='The organization to fetch the deployments.')
@deployment.command(name='deployment-detail', help='Detail a deployment.')
def detail(uid, organization):
    """
    Detail a deployment.
    :param uid: The deployment's uid
    :type uid: str
    :param organization: The deployment's organization.
    :type organization: str
    :returns: The status of the request.
    :rtype: bool
    """
    user = utils.get('user')
    organization = organization or '{}-default'.format(user)
    #1. Call the API to get the deployment detail
    status, infos = api.detail(uid, organization)
    if status:
        click.echo('Project\tBranch\tStatus\tCreation Date\n')
        for result in infos['results']:
            result = json.loads(result)
            click.echo('{0}\t{1}\t{2}'.format(
                result['name'],
                result['status'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)
