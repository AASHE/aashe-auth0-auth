import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

setup(
    name = 'auth0-auth',
    version = '0.0.1',
    url = 'https://github.com/aashe/aashe-auth0-auth',
    author = 'Dzemsad Dugalic',
    author_email = 'dzemsad.dugalic.fe@gmail.com',
    description = 'Authenticated users using Auth0.',
    long_description = get_readme(),
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    install_requires = read_file('requirements.txt'),
    classifiers = [
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Programming Language :: Python',
    ],
)