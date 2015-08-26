===============================
ConfigLoader
===============================

.. image:: https://img.shields.io/travis/adblair/configloader.svg
        :target: https://travis-ci.org/adblair/configloader

.. image:: https://coveralls.io/repos/adblair/configloader/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/adblair/configloader?branch=master

.. image:: https://img.shields.io/pypi/dm/configloader.svg
        :target: https://pypi.python.org/pypi/configloader

Python dict that supports common app configuration-loading scenarios.

Features
--------

Easily load configuration from:

* Modules
* JSON files
* YAML files
* Environment variables

Supports Python 2.6+ and 3.3+.

Example usage
-------------

    >>> from configloader import ConfigLoader
    >>> config = ConfigLoader
    >>> config.update_from_obj('my_app.settings')
    >>> config.update_from_json_file('config.json')


Documentation
-------------

https://configloader.readthedocs.org


.. _Flask: http://flask.pocoo.org/docs/0.10/config/#configuring-from-files
