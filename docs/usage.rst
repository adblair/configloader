========
Usage
========

Example usage::

    from configloader import ConfigLoader

    import myapp.default_settings

    config = ConfigLoader()
    config.update_from(
        obj=myapp.default_settings,
        yaml_env='MYAPP_SETTINGS_YAML',
    )
