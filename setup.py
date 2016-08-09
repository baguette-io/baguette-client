#-*- coding:utf-8 -*-
"""
Setup for baguette cli package.
"""
from setuptools import find_packages, setup

setup(
    name='baguette-client',
    version='0.1',
    url='baguette.io',
    download_url='baguette.io/get',
    author_email='dev@baguette.io',
    packages=find_packages(),
    platforms=[
        'Linux/UNIX',
        'MacOS',
        'Windows'
    ],
    install_requires=[
        'requests==2.10.0',
        'click==6.6',
        'GitPython==2.0.8',
    ],
    entry_points={
        'console_scripts':[
            'baguette=baguette.entrypoints:main',
        ],
    },
    extras_require={
        'test': [
            'mock==2.0.0',
            'pytest==2.9.2',
            'pytest-cov==2.3.0',
            'pylint==1.6.1',
        ],
        'doc': [
            'Sphinx==1.4.4',
        ],
    },
    package_data={
        'baguette':['baguette.ini'],
    },
)
