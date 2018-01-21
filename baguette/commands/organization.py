#-*-coding:utf-8 -*-
"""
Organization commands.
"""
import click
import baguette.api.organization as api
from .utils import display_errors

@click.group()
def organization():
    """
    Organization group commands.
    """

@click.argument('name')
@organization.command(name='organization-create', help='Create an organization.')
def create(name):
    """
    Create an organization.
    Idempotent.
    :param name: The organization name.
    :type name: str
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Call the API to create the organization
    created, infos = api.create(name)
    if created:
        click.echo('organization {0} created.'.format(name))
        return True
    return display_errors(infos)

@click.option('--offset', default=0, type=int, help='The offset to start retrieving the organization from.')
@click.option('--limit', default=10, type=int, help='The number of organizations per request.')
@organization.command(name='organization-list', help='List all the organizations.')
def find(offset, limit):
    """
    List all the organizations.
    :param limit: The number of organizations per request.
    :type limit: int
    :param offset: The offset to start to retrieve the organizations from.
    :type offset: int
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the organizations
    status, infos = api.find(limit, offset)
    if status:
        click.echo('\nstarting {0}, listing {1} organizations on a total of {2} organizations.\n'.format(
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Name\tDeletable\tCreation Date\n')
        for result in infos['results']:
            click.echo('{0}\t{1}\t{2}'.format(
                result['name'],
                result['deletable'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)

@click.argument('name')
@organization.command(name='organization-delete', help='Delete an organization.')
def delete(name):
    """
    Delete an organization.
    :param name: The organization name to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: bool
    """
    #1. Call the API to delete the organization
    deleted, infos = api.delete(name)
    if deleted:
        click.echo('organization {0} deleted.'.format(name))
        return True
    return display_errors(infos)
