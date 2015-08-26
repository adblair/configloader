# -*- coding: utf-8 -*-

import contextlib
import os
import tempfile
import textwrap

import py.test

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


@py.test.fixture
def config_loader():
    return ConfigLoader()


@contextlib.contextmanager
def temp_config_file(test_data):
    with tempfile.NamedTemporaryFile('wt') as configfile:
        configfile.write(test_data)
        configfile.seek(0)
        yield configfile.name


class TestConfigLoader:

    def test_init(self):
        config = ConfigLoader(logger=1)
        assert config.logger == 1

    def test_update_from(self):
        pass

    def test_update_from_obj(self):
        config = ConfigLoader()
        obj = Object()
        obj.setting = 'value'
        obj.SETTING = 'value'
        config.update_from_obj(obj)
        assert config == {'SETTING': 'value'}

    def test_update_from_yaml_env(self, config_loader, monkeypatch):
        with temp_config_file(test_yaml) as yaml_filename:
            monkeypatch.setenv('CONFIG_YAML', yaml_filename)
            config_loader.update_from_yaml_env('CONFIG_YAML')
        assert config_loader == test_config1

    def test_update_from_yaml_file(self, config_loader):
        with temp_config_file(test_yaml) as yaml_filename:
            config_loader.update_from_yaml_file(yaml_filename)
        assert config_loader == test_config1

    def test_update_from_json_env(self, config_loader, monkeypatch):
        with temp_config_file(test_json) as json_filename:
            monkeypatch.setenv('CONFIG_JSON', json_filename)
            config_loader.update_from_json_env('CONFIG_JSON')
        assert config_loader == test_config1

    def test_update_from_json_file(self, config_loader):
        with temp_config_file(test_json) as json_filename:
            config_loader.update_from_json_file(json_filename)
        assert config_loader == test_config1

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
