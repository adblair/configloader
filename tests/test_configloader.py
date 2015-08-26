# -*- coding: utf-8 -*-

import contextlib
import os
import tempfile
import textwrap

import mock
import py.test

from configloader import ConfigLoader


class test_obj:
    setting0 = 1
    SETTING0 = 2
    SETTING1 = 'blah'


test_obj_py = {
    'SETTING0': 2,
    'SETTING1': 'blah',
}


test_yaml = textwrap.dedent("""
    SETTING1: x
    SETTING2:
      - 1
      - 2
    SETTING3:
      foo: bar
""").strip()

test_yaml_py = {
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': {'foo': 'bar'},
}


test_json = textwrap.dedent("""
    {
        "SETTING3": "x",
        "SETTING4": [1, 2],
        "SETTING5": {"foo": "bar"}
    }
""").strip()

test_json_py = {
    'SETTING3': 'x',
    'SETTING4': [1, 2],
    'SETTING5': {'foo': 'bar'},
}


test_env = {
    'APP_SETTING5': 'x',
    'APP_SETTING6': 'y',
    'APP_SETTING7': 'z',
}

test_env_py = {
    'SETTING5': 'x',
    'SETTING6': 'y',
    'SETTING7': 'z',
}


test_combined_py = {
    'SETTING0': 2,
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': 'x',
    'SETTING4': [1, 2],
    'SETTING5': 'x',
    'SETTING6': 'y',
    'SETTING7': 'z',
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

    @mock.patch('configloader.ConfigLoader.update_from_obj')
    @mock.patch('configloader.ConfigLoader.update_from_yaml_env')
    @mock.patch('configloader.ConfigLoader.update_from_yaml_file')
    @mock.patch('configloader.ConfigLoader.update_from_json_env')
    @mock.patch('configloader.ConfigLoader.update_from_json_file')
    @mock.patch('configloader.ConfigLoader.update_from_env_namespace')
    def test_update_from_calls(
            self,
            mock_ufen,
            mock_ufjf,
            mock_ufje,
            mock_ufyf,
            mock_ufye,
            mock_ufo,
            config_loader
            ):
        """Check that the expected functions are called."""
        config_loader.update_from(
            obj=1,
            yaml_env=2,
            yaml_file=3,
            json_env=4,
            json_file=5,
            env_namespace=6,
        )
        mock_ufo.assert_called_with(1)
        mock_ufye.assert_called_with(2)
        mock_ufyf.assert_called_with(3)
        mock_ufje.assert_called_with(4)
        mock_ufjf.assert_called_with(5)
        mock_ufen.assert_called_with(6)

    def test_update_from_merge(self, config_loader, monkeypatch):
        """Check that config chunks are applied in the expected order."""
        for key, value in test_env.items():
            monkeypatch.setenv(key, value)
        with temp_config_file(test_yaml) as yaml_filename, \
                temp_config_file(test_json) as json_filename:
            config_loader.update_from(
                obj=test_obj,
                yaml_file=yaml_filename,
                json_file=json_filename,
                env_namespace='APP'
            )
        assert config_loader == test_combined_py

    def test_update_from_obj(self, config_loader):
        config_loader.update_from_obj(test_obj)
        assert config_loader == test_obj_py

    def test_update_from_yaml_env(self, config_loader, monkeypatch):
        with temp_config_file(test_yaml) as yaml_filename:
            monkeypatch.setenv('CONFIG_YAML', yaml_filename)
            config_loader.update_from_yaml_env('CONFIG_YAML')
        assert config_loader == test_yaml_py

    def test_update_from_yaml_file(self, config_loader):
        with temp_config_file(test_yaml) as yaml_filename:
            config_loader.update_from_yaml_file(yaml_filename)
        assert config_loader == test_yaml_py

    def test_update_from_json_env(self, config_loader, monkeypatch):
        with temp_config_file(test_json) as json_filename:
            monkeypatch.setenv('CONFIG_JSON', json_filename)
            config_loader.update_from_json_env('CONFIG_JSON')
        assert config_loader == test_json_py

    def test_update_from_json_file(self, config_loader):
        with temp_config_file(test_json) as json_filename:
            config_loader.update_from_json_file(json_filename)
        assert config_loader == test_json_py

    def test_update_from_env_namespace(self):
        config = ConfigLoader()
        os.environ.update(test_env)
        config.update_from_env_namespace('APP')
        for key in test_env:
            del os.environ[key]
        assert config == test_env_py

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
