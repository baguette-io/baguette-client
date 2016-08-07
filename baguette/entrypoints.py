#-*- coding:utf-8 -*-
"""
Contains all the baguette entrypoints.
"""
import click
import baguette.api
import baguette.settings

@click.group()
def general():
    """
    General commands.
    """

@click.argument('email', required=False)
@general.command()
def login(email):
    """
    Connect to baguette.io using their email/password.
    """
    if email:
        click.echo('Welcome {0}, please enter your baguette.io password.'.format(email))
    else:
        click.echo('Please enter your baguette.io credentials.')
        email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    if baguette.api.login(email, password):
        return click.echo('Successfully logged in as {0}.'.format(email))
    return click.echo('Authentication failed, please check your credentials.')

def main():
    """
    Baguette CLI.
    """
    baguette.settings.load()
    return click.CommandCollection(sources=[general])()
