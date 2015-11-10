# coding=UTF-8

import sqlite3

from converters import *
from dumper import Dumper

DEFAULT_TYPE = 'VARCHAR(1024)'
_converter_to_map = {
    empty_converter: DEFAULT_TYPE,
    int_convert: 'int',
}


class SqliteDumper(Dumper):
    def __init__(self, path_or_url, attr_list):
        Dumper.__init__(self, path_or_url, attr_list)
        self.connection = None
        self.init_sql = self.generate_init_sql()
        self.attribute_names = map(lambda a: format_attr_name(a), self.attr_list)
        self.insert_sql = self.generate_insert_sql()
        print self.insert_sql

    def init(self):
        self.connection = sqlite3.connect(self.path_or_url)
        self.connection.execute(self.init_sql)

    def generate_init_sql(self):
        fields = []
        for attr in self.attr_list:
            attribute_name, converter = extract_attr_converter(attr)
            fields.append(
                format_attr_name(attribute_name) + ' ' + _converter_to_map.get(get_converter(converter), DEFAULT_TYPE))
        return 'CREATE TABLE {0} ({1})'.format(self.collection_name, ', '.join(fields))

    def save_packet(self, packet_attributes):
        self.connection.execute(self.insert_sql,
                                map(lambda a: packet_attributes.get(a, None), self.attribute_names))
        self.connection.commit()

    def close(self):
        self.connection.close()

    def generate_insert_sql(self):
        return "INSERT INTO {0} ({1}) VALUES ({2})".format(self.collection_name, ", ".join(self.attribute_names),
                                                           ", ".join(['?'] * len(self.attr_list)))
