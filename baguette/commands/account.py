#-*-coding:utf-8 -*-
"""
Accounts commands.
"""
import decimal
import os
import click
import baguette.api.account as api
from .utils import display_errors

@click.group()
def account():
    """
    Account group commands.
    """

@click.option('--password',
              prompt=True,
              hide_input=True,
              confirmation_prompt=True)
@click.option('--email', prompt=True)
@click.option('--username',
              prompt=True,
              default=lambda: os.environ.get('USER', ''))
@account.command()
def signup(username, email, password):
    """
    Create an account on baguette.io.
    :param email: The email to signup with.
    :type email: str
    :param username: The username to signup in with.
    :type username: str
    :param password: The password to signup in with.
    :type password: str
    :returns: The status of the signup.
    :rtype: bool
    """
    status, infos = api.signup(email, username, password)
    if status:
        click.echo('Successfully signup to baguette.io.')
        click.echo('A RSA 4096 bits key has been generated in your ~/.ssh folder.')
        click.echo('\nYou can now login using `baguette login`.')
        return True
    return display_errors(infos)


@click.argument('email', required=False)
@account.command()
def login(email):
    """
    Connect to baguette.io using email/password.
    :param email: The email to log in with.
    :type email: str
    :returns: The status of the login.
    :rtype: bool
    """
    if email:
        click.echo('Welcome {0}, please enter your baguette.io password.'.format(email))
    else:
        click.echo('Please enter your baguette.io credentials.')
        email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    if api.login(email, password):
        #click.echo('Successfully logged in as {0}. Credentials expire in 1 hour.'.format(email))
        click.echo('Successfully logged in as {0}.'.format(email))
        return True
    click.echo('Authentication failed, please check your credentials.')
    return False

@account.command(name='quotas')
def quotas():
    """
    List all the account quotas.
    :returns: The status of the request.
    :rtype: bool
    """
    #1. Call the API to get all the keys
    status, infos = api.quotas()
    if status:
        click.echo('Name\tMax\tCreation Date\n')
        for result in infos['results']:
            click.echo('{0}\t{1}\t{2}'.format(
                result['key'],
                int(decimal.Decimal(result['value'])),
                result['date_created']))
            click.echo('')
        return True
    return display_errors(infos)
