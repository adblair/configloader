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

test_config1 = {
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': {'foo': 'bar'},
}

test_env = {
    'APP_SETTING1': 'x',
    'APP_SETTING2': 'y',
    'APP_SETTING3': 'z',
}

test_config2 = {
    'SETTING1': 'x',
    'SETTING2': 'y',
    'SETTING3': 'z',
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

    def test_init(self):
        config = ConfigLoader(logger=1)
        assert config.logger == 1

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
        assert config == test_config1

    def test_update_from_yaml_file(self):
        config = ConfigLoader()
        load_test_data(config, test_yaml, 'update_from_yaml_file', 'file')
        assert config == test_config1

    def test_update_from_json_env(self):
        config = ConfigLoader()
        load_test_data(config, test_json, 'update_from_json_env', 'env')
        assert config == test_config1

    def test_update_from_json_file(self):
        config = ConfigLoader()
        load_test_data(config, test_json, 'update_from_json_file', 'file')
        assert config == test_config1

    def test_update_from_env_namespace(self):
        config = ConfigLoader()
        os.environ.update(test_env)
        config.update_from_env_namespace('APP')
        for key in test_env:
            del os.environ[key]
        assert config == test_config2

    def test_namespace(self):
        config = ConfigLoader(
            PART1_SETTING1='x',
            PART1_SETTING2='y',
            PART2_SETTING1='z',
        )
        assert config.namespace('PART1') == dict(
            SETTING1='x',
            SETTING2='y',
        )
