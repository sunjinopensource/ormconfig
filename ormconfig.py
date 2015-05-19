import sys
import inspect
import codecs


__version__ = '0.1.0'


_PY2 = sys.version_info[0] == 2
_PY3 = sys.version_info[0] == 3
if _PY3:
    import configparser as _config_parser
    _config_read_file = _config_parser.ConfigParser.read_file
elif _PY2:
    import ConfigParser as _config_parser
    _config_read_file = _config_parser.ConfigParser.readfp
else:
    raise RuntimeError('Unsupported python version.')


def _transform_ip(s):
    ip = ''
    vec = s.split('.')
    if len(vec) != 4:
        return None
    for index, item in enumerate(vec):
        try:
            seg = int(item)
        except:
            return None
        if not (0 <= seg <= 255):
            return None
        ip += str(seg)
        if index != 3:
            ip += '.'
    return ip


def _transform_port(s):
    try:
        port = int(s)
    except:
        return None
    if not 0 <= port <= 65535:
        return None
    return port


class Error(Exception):
    pass


class Field:
    def __init__(self, default=None):
        self.default = default

    def to_python_value(self, value):
        return self.coerce(value)


class BoolField(Field):
    coerce = bool


class IntField(Field):
    coerce = int


class FloatField(Field):
    coerce = float


class StringField(Field):
    def __init__(self, allow_empty=False):
        self.allow_empty = allow_empty

    def coerce(self, value):
        if (not self.allow_empty) and (not value):
            raise ValueError('empty string not allowed')
        return value


class IPField(Field):
    def coerce(self, value):
        ip = _transform_ip(value)
        if ip is None:
            raise ValueError('ip must be <n>.<n>.<n>.<n> n between 0~255')
        return ip


class IPPortField(Field):
    def coerce(self, value):
        if ':' not in value:
            raise ValueError('format must be <ip>:<port>')

        vec = value.split(':')
        if len(vec) != 2:
            raise ValueError('format must be <ip>:<port>')

        ip = _transform_ip(vec[0])
        if ip is None:
            raise ValueError('ip must be <n>.<n>.<n>.<n> n between 0~255')

        port = _transform_port(vec[1])
        if port is None:
            raise ValueError('port must be a number between 0~65535')

        return (ip, port)


class Section:
    pass


class Config:
    @classmethod
    def load(cls, file_path, encoding='UTF-8'):
        conf = _config_parser.ConfigParser()

        try:
            fp = codecs.open(file_path, 'r', encoding)
            _config_read_file(conf, fp)
        except Exception as e:
            raise Error(str(e))

        ret = cls()
        for section_name, section_cls in cls.__dict__.items():
            if not (inspect.isclass(section_cls) and issubclass(section_cls, Section)):
                continue

            section = section_cls()
            setattr(ret, section_name, section)

            for field_name, field in section_cls.__dict__.items():
                if not isinstance(field, Field):
                    continue

                try:
                    origin_value = conf.get(section_name, field_name)
                    if _PY2:
                        origin_value = origin_value.encode(encoding)
                except (_config_parser.NoSectionError, _config_parser.NoOptionError) as e:
                    if field.default is None:
                        raise Error(str(e))
                    else:
                        origin_value = field.default

                try:
                    value = field.to_python_value(origin_value)
                except Exception as e:
                    raise Error("[%s] %s: '%s' is not a valid value of '%s': %s" % (
                        section_name, field_name, origin_value, field.__class__.__name__,
                        str(e)
                    ))

                setattr(section, field_name, value)

        return ret
