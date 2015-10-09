# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import contextlib
import io
import tempfile
import textwrap

import mock
import py.test

from configloader import ConfigLoader


class test_obj:
    setting0 = 1
    SETTING0 = 2
    SETTING1 = 'blah'

test_obj_output = {
    'SETTING0': 2,
    'SETTING1': 'blah',
}

test_obj_output_no_criterion = {
    'setting0': 1,
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
    NON_ASCII: ইঈউঊঋঌ
""").strip()

test_yaml_output = {
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': {'foo': 'bar'},
    'NON_ASCII': 'ইঈউঊঋঌ',
}


test_json = textwrap.dedent("""
    {
        "SETTING3": "x",
        "SETTING4": [1, 2],
        "SETTING5": {"foo": "bar"},
        "NON_ASCII": "ইঈউঊঋঌ"
    }
""").strip()

test_json_output = {
    'SETTING3': 'x',
    'SETTING4': [1, 2],
    'SETTING5': {'foo': 'bar'},
    'NON_ASCII': 'ইঈউঊঋঌ',
}


test_env = {
    'APP_SETTING5': 'x',
    'APP_SETTING6': 'y',
    'APP_SETTING7': 'z',
}

test_env_output = {
    'SETTING5': 'x',
    'SETTING6': 'y',
    'SETTING7': 'z',
}


test_combined_output = {
    'SETTING0': 2,
    'SETTING1': 'x',
    'SETTING2': [1, 2],
    'SETTING3': 'x',
    'SETTING4': [1, 2],
    'SETTING5': 'x',
    'SETTING6': 'y',
    'SETTING7': 'z',
    'NON_ASCII': 'ইঈউঊঋঌ',
}


test_config_namespace = {
    'PART1_SETTING1': 'x',
    'PART1_SETTING2': 'y',
    'PART2_SETTING1': 'z',
}

test_config_namespace_output_part1 = {
    'SETTING1': 'x',
    'SETTING2': 'y',
}

test_config_namespace_output_part1_lower = {
    'setting1': 'x',
    'setting2': 'y',
}


@py.test.fixture
def config_loader():
    return ConfigLoader()


@contextlib.contextmanager
def temp_config_file(test_data):
    with tempfile.NamedTemporaryFile('wb') as configfile:
        configfile.write(test_data.encode('utf-8'))
        configfile.seek(0)
        yield configfile.name


class TestConfigLoader:

    def test_init(self):
        config = ConfigLoader(logger=1)
        assert config.logger == 1

    @mock.patch('configloader.ConfigLoader.update_from_object')
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
        with temp_config_file(test_yaml) as yaml_filename:
            with temp_config_file(test_json) as json_filename:
                config_loader.update_from(
                    obj=test_obj,
                    yaml_file=yaml_filename,
                    json_file=json_filename,
                    env_namespace='APP'
                )
        assert config_loader == test_combined_output

    def test_update_from_object(self, config_loader):
        config_loader.update_from_object(test_obj)
        assert config_loader == test_obj_output

    def test_update_from_object_string(self, config_loader):
        imaginary_modules = {
            'my': mock.MagicMock(),
            'my.app': mock.MagicMock(settings=test_obj),
        }
        with mock.patch.dict('sys.modules', imaginary_modules):
            config_loader.update_from_object('my.app.settings')
        assert config_loader == test_obj_output

    def test_update_from_object_criterion(self, config_loader):
        config_loader.update_from_object(
            test_obj,
            criterion=lambda key: key[:1] not in ['_', '@']
        )
        assert config_loader == test_obj_output_no_criterion

    def test_update_from_yaml_env(self, config_loader, monkeypatch):
        with temp_config_file(test_yaml) as yaml_filename:
            monkeypatch.setenv('CONFIG_YAML', yaml_filename)
            config_loader.update_from_yaml_env('CONFIG_YAML')
        assert config_loader == test_yaml_output

    def test_update_from_yaml_file(self, config_loader):
        with temp_config_file(test_yaml) as yaml_filename:
            config_loader.update_from_yaml_file(yaml_filename)
        assert config_loader == test_yaml_output

    def test_update_from_yaml_file_obj(self, config_loader):
        config_loader.update_from_yaml_file(io.StringIO(test_yaml))
        assert config_loader == test_yaml_output

    def test_update_from_json_env(self, config_loader, monkeypatch):
        with temp_config_file(test_json) as json_filename:
            monkeypatch.setenv('CONFIG_JSON', json_filename)
            config_loader.update_from_json_env('CONFIG_JSON')
        assert config_loader == test_json_output

    def test_update_from_json_file(self, config_loader):
        with temp_config_file(test_json) as json_filename:
            config_loader.update_from_json_file(json_filename)
        assert config_loader == test_json_output

    def test_update_from_json_file_obj(self, config_loader):
        config_loader.update_from_json_file(io.StringIO(test_json))
        assert config_loader == test_json_output

    def test_update_from_env_namespace(self, config_loader):
        with mock.patch('os.environ', test_env):
            config_loader.update_from_env_namespace('APP')
        assert config_loader == test_env_output

    def test_namespace(self, config_loader):
        config_loader.update(test_config_namespace)
        assert config_loader.namespace('PART1') == \
            test_config_namespace_output_part1

    def test_namespace_lower(self, config_loader):
        config_loader.update(test_config_namespace)
        assert config_loader.namespace_lower('PART1') == \
            test_config_namespace_output_part1_lower
