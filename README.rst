ormconfig
=========

A little orm for config file, do transformation to/from python object

Examples
--------

example.ini::
	
    [Section1]
    bool_field = True
    int_field = 123
    float_field = 456.7
    string_field = hello, world

    [Section2]
    ip_field = 127.0.0.1
    ipport_field = 127.0.0.1:12345

example.py::

    from ormconfig import *
    import sys

    class MyConfig(Config):
        class Section1(Section):
            bool_field = BoolField()
            int_field = IntField()
            float_field = FloatField()
            string_field = StringField()
        class Section2(Section):
            ip_field = IPField()
            ipport_field = IPPortField()

    try:
        config = MyConfig.load('test.ini')
    except Error as e:
        print('Failed to load file: %s' % str(e))
        sys.exit(0)

    print(config.Section1.bool_field)
    print(config.Section1.int_field)
    print(config.Section1.float_field)
    print(config.Section1.string_field)
    print(config.Section2.ip_field)
    print(config.Section2.ipport_field)

output::

    True
    123
    456.7
    hello, world
    127.0.0.1
    ('127.0.0.1', 12345)
