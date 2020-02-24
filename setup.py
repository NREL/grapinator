#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import os

def get_textfile(filename):
    """ Get contents from a text file. """
    with open(filename, 'r') as fh:
        return fh.read().lstrip()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        print("Calling PostDevelopCommand(develop)")
        from flask_graphql import graphqlview
        path = os.path.abspath(graphqlview.__file__)
        # call fix_flask_graphql.sh to remedy 500 error for badly formed unicode.  See docs/500_error.txt
        cmd = os.path.abspath(os.path.join(os.path.dirname(__file__), 'grapinator/resources/setup_fix/fix_flask_graphql.sh'))
        check_call([cmd, path])
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for install mode."""
    def run(self):
        print("Calling PostInstallCommand(install)")
        from flask_graphql import graphqlview
        path = os.path.abspath(graphqlview.__file__)
        # call fix_flask_graphql.sh to remedy 500 error for badly formed unicode.  See docs/500_error.txt
        cmd = os.path.abspath(os.path.join(os.path.dirname(__file__), 'grapinator/resources/setup_fix/fix_flask_graphql.sh'))
        check_call([cmd, path])
        install.run(self)

setup(
    name='grapinator',
    version='1.0.0.dev1',
    description='Dynamic GraphQL API Creator',
    long_description=get_textfile('README.md'),
    author='David Martin',
    packages=find_packages(),
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
