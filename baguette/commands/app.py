#-*-coding:utf-8 -*-
"""
App commands.
"""
import os
import click
import git
import baguette.api

@click.group()
def app():
    """
    App group commands.
    """

@click.argument('name', required=False)
@app.command(name='app create')
def create(name):
    """
    Create an app of the current git repo.
    Idempotent.
    :param name: The app name. Optional.
    :type name: None, str
    :returns: The status of the creation.
    :rtype: bool
    """
    #1. Check that we are currently in a git repo.
    try:
        git.Repo(os.getcwd())
    except git.exc.InvalidGitRepositoryError:
        click.echo('The current path is not a root git directory.')
        return False
    #2. Generate the name if not set
    name = name or os.path.basename(os.getcwd())
    click.echo('Creating {0}...'.format(name))
    #3. Call the API to create the app
    created = baguette.api.create(name)
    if created:
        baguette.api.git_init(created['repo_uri'])
        click.echo("""{0} created.
Automatically added `baguette.io` remote.
When pushing to this remote, your app will be automatically deployed.""".format(name))
        return True
    click.echo('Cannot create {0}. Are you still logged in ?'.format(name))
    return False

@app.command(name='app find')
def find():
    """
    List all the apps.
    """

@app.command(name='app delete')
def delete():
    """
    Delete an app.
    """
