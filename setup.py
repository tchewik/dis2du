#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
from os.path import dirname
from os.path import join

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='dis2du',
    packages=['dis2du'],
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['isanlp @ git+https://github.com/IINemo/isanlp.git']
)
