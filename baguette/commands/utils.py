#-*- coding:utf-8 -*-
"""
Utils for the commands.
"""
import click

def display_errors(errors):
    """
    Given the errors, display them.
    :param errors: The errors returned by the API.
    :type errors: dict
    """
    for field, msg in errors.iteritems():
        field = field if field != 'non_field_errors' else 'general'
        if field == 'detail' and  msg == 'Signature has expired.':
            field = 'general'
            msg = 'Session has expired. Please login again.'
        click.echo('{0} : {1}'.format(field, ''.join(msg)))
    return False
