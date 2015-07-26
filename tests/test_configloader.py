# -*- coding: utf-8 -*-

import os
import tempfile
import textwrap

from configloader import ConfigLoader


class Object(object):
    pass


test_yaml = textwrap.dedent("""
    SETTING1: x
    SETTING2:
      - 1
      - 2
    SETTING3:
      foo: bar
""").strip()

test_json = textwrap.dedent("""
    {
        "SETTING1": "x",
        "SETTING2": [1, 2],
        "SETTING3": {"foo": "bar"}
    }
""").strip()

test_config = {
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': {'foo': 'bar'},
}


def load_test_data(config_loader, test_data, load_func, method):
    with tempfile.NamedTemporaryFile('wt') as configfile:
        configfile.write(test_data)
        configfile.seek(0)
        if method == 'file':
            getattr(config_loader, load_func)(configfile.name)
        elif method == 'env':
            os.environ['TEMP_FILEPATH'] = configfile.name
            getattr(config_loader, load_func)('TEMP_FILEPATH')
            del os.environ['TEMP_FILEPATH']


class TestConfigLoader:

    def test_update_from_obj(self):
        config = ConfigLoader()
        obj = Object()
        obj.setting = 'value'
        obj.SETTING = 'value'
        config.update_from_obj(obj)
        assert config == {'SETTING': 'value'}

    def test_update_from_yaml_env(self):
        config = ConfigLoader()
        load_test_data(config, test_yaml, 'update_from_yaml_env', 'env')
        assert config == test_config

    def test_update_from_yaml_file(self):
        config = ConfigLoader()
        load_test_data(config, test_yaml, 'update_from_yaml_file', 'file')
        assert config == test_config

    def test_update_from_json_env(self):
        config = ConfigLoader()
        load_test_data(config, test_json, 'update_from_json_env', 'env')
        assert config == test_config

    def test_update_from_json_file(self):
        config = ConfigLoader()
        load_test_data(config, test_json, 'update_from_json_file', 'file')
        assert config == test_config
