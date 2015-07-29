#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

extras_require = {
    'yaml':  ["PyYAML>=3"],
    'attrdict': ["attrdict>=1"],
}

extras_require.update(all=sorted(set().union(*extras_require.values())))

setup(
    name='configloader',
    version='0.1.1',
    description=(
        "Python dict that supports common app configuration-loading scenarios."
    ),
    long_description=readme + '\n\n' + history,
    author="Arthur Blair",
    author_email='adblair@gmail.com',
    url='https://github.com/adblair/configloader',
    packages=[
        'configloader',
    ],
    package_dir={'configloader':
                 'configloader'},
    include_package_data=True,
    install_requires=requirements,
    extras_require = extras_require,
    license="MIT",
    zip_safe=False,
    keywords='configloader',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
    test_suite='tests',
    tests_require=test_requirements
)
