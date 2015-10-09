#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

extras_require = {
    'attrdict': ["attrdict>=1"],
    'yaml':  ["PyYAML>=3"],
}

extras_require.update(all=sorted(set().union(*extras_require.values())))

setup(
    name='configloader',
    version='1.0.0.dev1',
    packages=find_packages(),
    extras_require=extras_require,

    author="Arthur Blair",
    author_email='adblair@gmail.com',
    url='https://github.com/adblair/configloader',
    description=(
        "Python dict that supports common app configuration-loading scenarios."
    ),
    long_description=readme,
    license="MIT",
    zip_safe=False,
    keywords='configloader',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
