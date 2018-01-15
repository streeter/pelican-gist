#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pelican_gist


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'pelican_gist',
]

requires = [
    'requests>=2.2.0',
    'pygments'
]

tests_require = [
    'mock>=1.0.1'
]

setup(
    name='pelican-gist',
    version=pelican_gist.__version__,
    description='Easily embed GitHub Gists in your Pelican articles.',
    long_description=readme,
    author='Chris Streeter',
    author_email='chris@chrisstreeter.com',
    url='https://github.com/streeter/pelican-gist',
    packages=packages,
    package_data={'': ['LICENSE', ]},
    package_dir={'pelican_gist': 'pelican_gist'},
    include_package_data=True,
    install_requires=requires,
    tests_require=tests_require,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
)
