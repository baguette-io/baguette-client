#-8- coding:utf-8 -*-
"""
Module containing the configuration.
"""
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
import os

def load():
    """
    Load the tiny configuration
    from the ini file.
    """
    parser = configparser.RawConfigParser()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'baguette.ini')
    parser.readfp(open(path))
    for section in parser.sections():
        globals()[section] = {}
        for key, val in parser.items(section):
            globals()[section][key] = val
