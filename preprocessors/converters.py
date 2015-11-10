# coding=UTF-8

import types


def format_attr_name(attr_name_dot):
    attr = attr_name_dot
    if isinstance(attr, types.StringTypes):
        return attr.replace('.', '_')
    elif isinstance(attr, (types.TupleType, types.ListType)):
        return attr[0].replace('.', '_')
    else:
        raise Exception("属性描述类别不支持" + str(type(attr)))


def extract_attr_converter(attr):
    if isinstance(attr, types.StringTypes):
        return attr, empty_converter
    elif isinstance(attr, (types.TupleType, types.ListType)):
        return attr[0], get_converter(attr[1])
    else:
        raise Exception("属性描述类别不支持" + str(type(attr)))


def get_converter(converter):
    if not converter:
        return empty_converter

    if callable(converter):
        return converter

    if isinstance(converter, types.StringTypes):
        return _converter_map.get(converter, empty_converter)

    return empty_converter


def empty_converter(o):
    return o


def string_converter(o):
    return str(o)


def int_convert(o):
    return int(o)


def float_convert(o):
    return float(o)


_converter_map = {
    'string': string_converter,
    'int': int_convert,
    'float': float_convert
}

