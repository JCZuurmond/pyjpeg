#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


import setuptools


with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = []
setup_requirements = [
    'pytest-runner',
]
test_requirements = [
    'pytest',
    'pytest-cov',
]
extra_requirements = {
    'dev': ['pre-commit', 'flake8']
}


setuptools.setup(
    name='pyjpeg',
    author='Cor Zuurmond',
    author_email='jczuurmond@protonmail.com',
    description='JPEG implementation in Python.',
    url='https://github.com/JCZuurmond/pyjpeg',
    license='Open source',
    packages=setuptools.find_packages('pyjpeg'),
    version='0.1.0',
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require=extra_requirements,
)
