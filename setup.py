#-*- coding:utf-8 -*-
"""
Setup for baguette cli package.
"""
from setuptools import find_packages, setup

setup(
    name='baguette-client',
    version='0.11',
    description='Baguette Command Line Interface',
    long_description=open('README.rst').read(),
    keywords=['cli', 'baguette'],
    url='https://github.com/baguette-io/baguette-client/',
    author_email='pydavid@baguette.io',
    classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
      ],
    packages=find_packages(),
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
        'testing': [
            'mock==2.0.0',
            'pytest==3.3.2',
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
