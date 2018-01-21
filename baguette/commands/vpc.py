#-*-coding:utf-8 -*-
"""
namespaces commands.
"""
import click
import baguette.api.vpc as api
from .utils import display_errors

@click.group()
def vpc():
    """
    Namespace group commands.
    """

@click.option('--organization', default=None, type=str, help='The namespace organization.')
@click.argument('name')
@vpc.command(name='namespace-create', help='Create a namespace.')
def create(name, organization):
    """
    Create a namespace.
    Idempotent.
    :param name: The namespace name.
    :type name: str
    :param organization: The namespace's organization.
    :type organization: str
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Call the API to create the namespace
    organization  'default'
    created, infos = api.create(name, organization)
    if created:
        click.echo('{0} : namespace {1} created.'.format(organization, name))
        return True
    return display_errors(infos)

@click.option('--offset', default=0, type=int, help='The offset to start retrieving the namespace from.')
@click.option('--limit', default=10, type=int, help='The number of namespaces per request.')
@vpc.command(name='namespace-list', help='List all the namespaces.')
def find(offset, limit):
    """
    List all the namespaces.
    :param limit: The number of namespaces per request.
    :type limit: int
    :param offset: The offset to start to retrieve the namespaces from.
    :type offset: int
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the namespaces
    status, infos = api.find(limit, offset)
    if status:
        click.echo('Starting {0}, listing {1} namespaces on a total of {2} namespaces.'.format(
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
@vpc.command(name='namespace-delete', help='Delete a namespace.')
def delete(name):
    """
    Delete a namespace.
    :param name: The namespace name to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: bool
    """
    #1. Call the API to delete the namespace
    deleted, infos = api.delete(name)
    if deleted:
        click.echo('namespace {0} deleted.'.format(name))
        return True
    return display_errors(infos)
