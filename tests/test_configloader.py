# -*- coding: utf-8 -*-

from configloader import ConfigLoader


class Object(object):
    pass


class TestConfigLoader:

    def test_update_from_obj(self):
        config = ConfigLoader()
        obj = Object()
        obj.setting = 'value'
        obj.SETTING = 'value'
        config.update_from_obj(obj)
        assert config == {'SETTING': 'value'}
