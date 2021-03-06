ormconfig
=========

A little orm for config file, do transformation to/from python object

Examples
--------

example.ini::
	
    [Section1]
    bool_field = True
    int_field = 123
    #int_default_field = 567
    float_field = 456.7
    string_field = hello, world

    [Section2]
    ip_field = 127.0.0.1
    ipport_field = 127.0.0.1:12345
    ipport_list_field = 127.0.0.1:12345, 127.0.0.2:12346
	
	[Section3]
	choice_field = release

example.py::

    from ormconfig import *
    import sys

    class MyConfig(Config):
        class Section1(Section):
            bool_field = BoolField()
            int_field = IntField()
            int_default_field = IntField(default='default value 6')
            float_field = FloatField()
            string_field = StringField()
        class Section2(Section):
            ip_field = IPField()
            ipport_field = IPPortField()
            ipport_list_field = ListField(IPPortField())
        class Section3(Section):
			choice_field = ChoiceField(StringField(), ['debug', 'release'], 'debug')

    try:
        config = MyConfig.load('example.ini')
    except Error as e:
        print('Failed to load file: %s' % str(e))
        sys.exit(1)

    print(config.Section1.bool_field)
    print(config.Section1.int_field)
    print(config.Section1.int_default_field)
    print(config.Section1.float_field)
    print(config.Section1.string_field)
    print(config.Section2.ip_field)
    print(config.Section2.ipport_field)
    print(config.Section2.ipport_list_field)
	print(config.Section3.choice_field)

output::

    True
    123
    default value 6
    456.7
    hello, world
    127.0.0.1
    ('127.0.0.1', 12345)
    [('127.0.0.1', 12345), ('127.0.0.2', 12346)]
	release
