# coding=UTF-8

import silk
from extractor import Extractor
from converters import extract_attr_converter, format_attr_name


class SilkExtractor(Extractor):
    def __init__(self):
        Extractor.__init__(self)

    def extract(self, source, attr_list, **kwargs):
        silk_file = silk.SilkFile(source, silk.READ)
        try:
            attr_name_list = map(format_attr_name, attr_list)
            attr_converter_list = map(extract_attr_converter, attr_list)
            for record in silk_file:
                attributes = dict()
                for i, attr_desc in enumerate(attr_list):
                    attr_name, converter = attr_converter_list[i]
                    orig_value = getattr(record, attr_name)
                    # handle silk specified types
                    orig_value = self.convert(orig_value)
                    attributes[attr_name_list[i]] = converter(orig_value)
                yield attributes
        finally:
            silk_file.close()

    @staticmethod
    def convert(v):
        if isinstance(v, (silk.IPv4Addr, silk.IPv6Addr)):
            return str(v)
        return v

    def all_attributes(self):
        return _all_attributes


_all_attributes = filter(lambda n: not n.startswith('_') and not callable(getattr(silk.RWRec, n)), dir(silk.RWRec))
