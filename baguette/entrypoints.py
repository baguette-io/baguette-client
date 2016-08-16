#-*- coding:utf-8 -*-
"""
Contains all the baguette entrypoints.
"""
import os
import git
import click
import baguette.api
import baguette.settings

@click.group()
def general():
    """
    General commands.
    """

@click.option('--password',
              prompt=True,
              hide_input=True,
              confirmation_prompt=True)
@click.option('--email', prompt=True)
@click.option('--username',
              prompt=True,
              default=lambda: os.environ.get('USER', ''))
@general.command()
def signup(username, email, password):
    """
    Create an account on baguette.io
    :param email: The email to signup with.
    :type email: str
    :param username: The username to signup in with.
    :type username: str
    :param password: The password to signup in with.
    :type password: str
    :returns: The status of the signup.
    :rtype: bool
    """
    status, infos = baguette.api.signup(email, username, password)
    if status:
        click.echo('Successfully signup to baguette.io.\n'
                   'You can now login using `baguette login`.')
        return True
    click.echo('Signup Failed. Please verify your inputs.')
    for field, msg in infos.iteritems():
        field = field if field != 'non_field_errors' else 'general'
        click.echo('{0} : {1}'.format(field, ''.join(msg)))
    return False


@click.argument('email', required=False)
@general.command()
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
    if baguette.api.login(email, password):
        click.echo('Successfully logged in as {0}. Credentials expire in X minutes.'.format(email))
        return True
    click.echo('Authentication failed, please check your credentials.')
    return False

@click.argument('name', required=False)
@general.command()
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
        repo = git.Repo(os.getcwd())
    except git.exc.InvalidGitRepositoryError:
        click.echo('The current path is not a root git directory.')
        return False
    #2. Generate the name if not set
    name = name or os.path.basename(os.getcwd())
    click.echo('Creating {0}...'.format(name))
    #3. Call the API to create the app
    created = baguette.api.create(name)
    if created:
        #4. Add the remote if not yet added.
        if not any(r for r in repo.remotes if r.name == 'baguette.io'):
            repo.create_remote('baguette.io', created['repo_uri'])
        click.echo("""{0} created.
Automatically added `baguette.io` remote.
When pushing to this remote, your app will be automatically deployed.""".format(name))
        return True
    click.echo('Cannot create {0}. Are you still logged in ?'.format(name))
    return False

def main():
    """
    Baguette CLI.
    """
    baguette.settings.load()
    return click.CommandCollection(sources=[general])()
