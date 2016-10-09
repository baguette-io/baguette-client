#-*-coding:utf-8 -*-
"""
Keys commands.
"""
import click
import baguette.api.key as api
from .utils import display_errors

@click.group()
def key():
    """
    Key group commands.
    """

@click.argument('public', type=click.File())
@click.argument('name')
@key.command(name='key-create', help='Create a key.')
def create(name, public):
    """
    Create a key.
    :param name: The key name.
    :type name: str
    :param key: The public key.
    :type key: File
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Call the API to create the key
    created, infos = api.create(name, public)
    if created:
        click.echo('Key {0} created.'.format(name))
        return True
    return display_errors(infos)

@click.option('--offset', default=0, type=int, help='The offset to start retrieving the keys from.')
@click.option('--limit', default=10, type=int, help='The number of keys per request.')
@key.command(name='key-list', help='List all the keys.')
def find(offset, limit):
    """
    List all the keys.
    :param limit: The number of keys per request.
    :type limit: int
    :param offset: The offset to start to retrieve the keys from.
    :type offset: int
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the keys
    status, infos = api.find(limit, offset)
    if status:
        click.echo('Starting {0}, listing {1} keys on a total of {2} keys.'.format(
            offset,
            min(limit, infos['count']),
            infos['count']))
        click.echo('Name\tPublic key\tCreation Date\n')
        for result in infos['results']:
            click.echo('{0}\t{1}\t{2}'.format(
                result['name'],
                result['public'],
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)

@click.argument('name')
@key.command(name='key-delete', help='Delete a key.')
def delete(name):
    """
    Delete a key.
    :param name: The key name to delete.
    :type name: str
    :returns: The status of the deletion.
    :rtype: bool
    """
    #1. Call the API to delete the key
    deleted, infos = api.delete(name)
    if deleted:
        click.echo('Key {0} deleted.'.format(name))
        return True
    return display_errors(infos)
