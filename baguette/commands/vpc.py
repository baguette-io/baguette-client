#-*-coding:utf-8 -*-
"""
Vpcs commands.
"""
import click
import baguette.api.vpc as api
from .utils import display_errors

@click.group()
def vpc():
    """
    VPC group commands.
    """

@click.argument('name')
@vpc.command(name='vpc-create')
def create(name):
    """
    Create a vpc.
    Idempotent.
    :param name: The vpc name.
    :type name: str
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Call the API to create the vpc
    created, infos = api.create(name)
    if created:
        click.echo('Vpc {0} created.'.format(name))
        return True
    return display_errors(infos)

@click.argument('offset', default=0, type=int)
@click.argument('limit', default=10, type=int)
@vpc.command(name='vpc-list')
def find(offset, limit):
    """
    List all the vpcs.
    :param limit: The number of vpcs per request.
    :type limit: int
    :param offset: The offset to start to retrieve the vpcs from.
    :type offset: int
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the vpcs
    status, infos = api.find(limit, offset)
    if status:
        click.echo('Starting {0}, listing {1} vpcs on a total of {2} vpcs.'.format(
            offset,
            min(offset+limit, infos['count']),
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
@vpc.command(name='vpc-delete')
def delete(name):
    """
    Delete a vpc.
    :param name: The vpc name to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: bool
    """
    #1. Call the API to delete the vpc
    deleted, infos = api.delete(name)
    if deleted:
        click.echo('Vpc {0} deleted.'.format(name))
        return True
    return display_errors(infos)
