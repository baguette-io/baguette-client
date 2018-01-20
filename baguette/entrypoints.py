#-*- coding:utf-8 -*-
"""
Contains all the baguette entrypoints.
"""
import click
from baguette.commands import account, app, key, organization, vpc
import baguette.settings

def main():
    """
    Baguette CLI.
    """
    baguette.settings.load()
    return click.CommandCollection(sources=[account, app, key, organization, vpc])()
