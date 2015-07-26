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

        with tempfile.NamedTemporaryFile('wt') as yamlfile:
            yamlfile.write(test_yaml)
            yamlfile.seek(0)
            os.environ['TEST_YAML'] = yamlfile.name
            config.update_from_yaml_env('TEST_YAML')
            del os.environ['TEST_YAML']

        assert config == {
            'SETTING1': 'x',
            'SETTING2': [1, 2],
            'SETTING3': {'foo': 'bar'},
        }

    def test_update_from_yaml_file(self):
        config = ConfigLoader()

        with tempfile.NamedTemporaryFile('wt') as yamlfile:
            yamlfile.write(test_yaml)
            yamlfile.seek(0)
            config.update_from_yaml_file(yamlfile.name)

        assert config == {
            'SETTING1': 'x',
            'SETTING2': [1, 2],
            'SETTING3': {'foo': 'bar'},
        }
