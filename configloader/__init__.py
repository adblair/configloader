# -*- coding: utf-8 -*-

__author__ = 'Arthur Blair'
__email__ = 'adblair@gmail.com'
__version__ = '0.1.0'


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


class ConfigLoader(DictType):

    """A dict that supports common app configuration-loading scenarios."""

    def __init__(self, *args, **kwargs):
        self.logger = kwargs.pop('logger', logging.getLogger(__name__))
        super(ConfigLoader, self).__init__(*args, **kwargs)

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
            self.update_from_obj(obj)
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

    def update_from_obj(self, obj, criterion=lambda key: key.isupper()):
        self.logger.debug('Loading config from {0}'.format(obj))
        self.update(
            (key, getattr(obj, key))
            for key in filter(criterion, dir(obj))
        )

    def update_from_yaml_env(self, env_var):
        _check_yaml_module()
        return self._update_from_env(env_var, yaml.safe_load)

    def update_from_yaml_file(self, file_path_or_obj):
        _check_yaml_module()
        return self._update_from_file(file_path_or_obj, yaml.safe_load)

    def update_from_json_env(self, env_var):
        return self._update_from_env(env_var, json.load)

    def update_from_json_file(self, file_path_or_obj):
        return self._update_from_file(file_path_or_obj, json.load)

    def update_from_env_namespace(self, namespace):
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
            self.logger.debug(
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
            self.logger.debug(
                'Not loading config from {0}; file nonexistant'.format(
                    file_path
                )
            )

    def _update_from_file_obj(self, file_obj, loader):
        if hasattr(file_obj, 'name'):
            self.logger.debug('Loading config from {0}'.format(
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
