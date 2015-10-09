# -*- coding: utf-8 -*-

__author__ = 'Arthur Blair'
__email__ = 'adblair@gmail.com'
__version__ = '1.0.0.dev1'


import json
import logging
import os

try:
    import attrdict
except ImportError:
    pass
try:
    import yaml
except ImportError:
    pass

try:
    DictType = attrdict.AttrDict
except NameError:
    DictType = dict

# Set basestring as an alias for the base string type in Python 3
try:
    basestring
except NameError:
    basestring = str

log = logging.getLogger(__name__)


class ConfigLoader(DictType):

    """
    A dict that supports common app configuration-loading scenarios.

    If `AttrDict`_ is installed, then elements can be accessed as both keys
    and attributes.

    .. _AttrDict: https://github.com/bcj/AttrDict
    """

    def update_from(
            self,
            obj=None,
            yaml_env=None,
            yaml_file=None,
            json_env=None,
            json_file=None,
            env_namespace=None,
            ):
        if obj:
            self.update_from_object(obj)
        if yaml_env:
            self.update_from_yaml_env(yaml_env)
        if yaml_file:
            self.update_from_yaml_file(yaml_file)
        if json_env:
            self.update_from_json_env(json_env)
        if json_file:
            self.update_from_json_file(json_file)
        if env_namespace:
            self.update_from_env_namespace(env_namespace)

    def update_from_object(self, obj, criterion=lambda key: key.isupper()):
        """
        Update dict from the attributes of a module, class or other object.

        By default only attributes with all-uppercase names will be retrieved.
        Use the ``criterion`` argument to modify that behaviour.

        :arg obj: Either the actual module/object, or its absolute name, e.g.
            'my_app.settings'.

        :arg criterion: Callable that must return True when passed the name
            of an attribute, if that attribute is to be used.
        :type criterion: :py:class:`function`

        .. versionadded:: 1.0
        """
        log.debug('Loading config from {0}'.format(obj))
        if isinstance(obj, basestring):
            if '.' in obj:
                path, name = obj.rsplit('.', 1)
                mod = __import__(path, globals(), locals(), [name], 0)
                obj = getattr(mod, name)
            else:
                obj = __import__(obj, globals(), locals(), [], 0)
        self.update(
            (key, getattr(obj, key))
            for key in filter(criterion, dir(obj))
        )

    def update_from_yaml_env(self, env_var):
        """
        Update dict from the YAML file specified in an environment variable.

        The `PyYAML`_ package must be installed before this method can be used.

        :arg env_var: Environment variable name.
        :type env_var: :py:class:`str`

        .. _PyYAML: http://pyyaml.org/wiki/PyYAML
        """
        _check_yaml_module()
        return self._update_from_env(env_var, yaml.safe_load)

    def update_from_yaml_file(self, file_path_or_obj):
        """
        Update dict from a YAML file.

        The `PyYAML`_ package must be installed before this method can be used.

        :arg file_path_or_obj: Filepath or file-like object.

        .. _PyYAML: http://pyyaml.org/wiki/PyYAML
        """
        _check_yaml_module()
        return self._update_from_file(file_path_or_obj, yaml.safe_load)

    def update_from_json_env(self, env_var):
        """
        Update dict from the JSON file specified in an environment variable.

        :arg env_var: Environment variable name.
        :type env_var: :py:class:`str`
        """
        return self._update_from_env(env_var, json.load)

    def update_from_json_file(self, file_path_or_obj):
        """
        Update dict from a JSON file.

        :arg file_path_or_obj: Filepath or file-like object.
        """
        return self._update_from_file(file_path_or_obj, json.load)

    def update_from_env_namespace(self, namespace):
        """
        Update dict from any environment variables that have a given prefix.

        The common prefix is removed when converting the variable names to
        dictionary keys. For example, if the following environment variables
        were set::

            MY_APP_SETTING1=foo
            MY_APP_SETTING2=bar

        Then calling ``.update_from_env_namespace('MY_APP')`` would be
        equivalent to calling
        ``.update({'SETTING1': 'foo', 'SETTING2': 'bar'})``.

        :arg namespace: Common environment variable prefix.
        :type env_var: :py:class:`str`
        """
        self.update(ConfigLoader(os.environ).namespace(namespace))

    def namespace(self, namespace, key_transform=lambda key: key):
        namespace = namespace.rstrip('_') + '_'
        return ConfigLoader(
            (key_transform(key[len(namespace):]), value)
            for key, value in self.items()
            if key[:len(namespace)] == namespace
        )

    def namespace_lower(self, namespace):
        return self.namespace(namespace, key_transform=lambda key: key.lower())

    def _update_from_env(self, env_var, loader):
        if env_var in os.environ:
            self._update_from_file_path(os.environ[env_var], loader)
        else:
            log.debug(
                'Not loading config from {0}; variable not set'.format(env_var)
            )

    def _update_from_file(self, file_path_or_obj, loader):
        if hasattr(file_path_or_obj, 'read'):
            self._update_from_file_obj(file_path_or_obj, loader)
        else:
            self._update_from_file_path(file_path_or_obj, loader)

    def _update_from_file_path(self, file_path, loader):
        if os.path.exists(file_path):
            with open(file_path) as file_obj:
                self._update_from_file_obj(file_obj, loader)
        else:
            log.debug(
                'Not loading config from {0}; file nonexistant'.format(
                    file_path
                )
            )

    def _update_from_file_obj(self, file_obj, loader):
        if hasattr(file_obj, 'name') and isinstance(file_obj.name, basestring):
            log.debug('Loading config from {0}'.format(
                os.path.abspath(file_obj.name)
            ))
        self.update(loader(file_obj))

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, dict.__repr__(self))


def _check_yaml_module():
    try:
        yaml
    except NameError:
        raise ImportError(
            'yaml module not found; please install PyYAML in order to enable '
            'configuration to be loaded from YAML files',
            name='yaml',
            path=__file__,
        )
