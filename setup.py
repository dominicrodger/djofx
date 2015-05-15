#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import djofx

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


version = djofx.__version__
readme = open('README.rst').read()

setup(
    name='djofx',
    version=version,
    description="""A Django app for tracking your finances.""",
    long_description=readme,
    author='Dominic Rodger',
    author_email='internet@dominicrodger.com',
    url='https://github.com/dominicrodger/djofx',
    packages=[
        'djofx',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='djofx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=[
        "pytest==2.6.4",
        "pytest-cov==1.7.0",
        "pytest-django==2.8.0",
    ],
    cmdclass={'test': PyTest},
)
