============
ConfigLoader
============

.. image:: https://travis-ci.org/adblair/configloader.svg?branch=master
        :target: https://travis-ci.org/adblair/configloader

.. image:: https://coveralls.io/repos/adblair/configloader/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/adblair/configloader?branch=master

.. image:: https://img.shields.io/pypi/dm/configloader.svg
        :target: https://pypi.python.org/pypi/configloader

ConfigLoader is a Python dictionary subclass that provides convenience methods
for common app configuration-loading scenarios, inspired by `flask.Config`_.


Features
--------

Easily load config settings from:

* Python modules, classes or objects
* JSON files
* YAML files
* Environment variables

Supports Python 2.6+ and 3.3+.


Installation
------------

Install ConfigLoader from `PyPI`_ using `pip`_::

    pip install configloader[all]

The ``[all]`` indicates that all optional dependencies (AttrDict and PyYAML)
should be installed.


Example usage
-------------

::

    >>> from configloader import ConfigLoader
    >>> config = ConfigLoader
    >>> config.update_from_object('my_app.settings')
    >>> config.update_from_yaml_file('config.yml')


Documentation
-------------

https://configloader.readthedocs.org


.. _flask.Config: http://flask.pocoo.org/docs/0.10/api/#configuration
.. _PyPI: https://pypi.python.org/pypi
.. _pip: https://pip.pypa.io/
