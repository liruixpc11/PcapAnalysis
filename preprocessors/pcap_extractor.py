# coding=UTF-8
import types

import scapy.all
from scapy.all import Packet, PcapReader
from preprocessors.converters import extract_attr_converter, format_attr_name
from preprocessors.extractor import Extractor


class PcapExtractor(Extractor):
    def extract(self, source, attr_list, **kwargs):
        return extract_attributes(source, attr_list, **kwargs)

    def all_attributes(self):
        return _all_attributes


def extract_all_protocols():
    protocol_map = dict()
    for name, e in scapy.all.__dict__.items():
        if isinstance(e, types.TypeType) and issubclass(e, Packet):
            protocol_map[name.lower()] = {
                "class": e,
                "fields": map(lambda f: f.name, e.fields_desc)
            }
    return protocol_map


_protocol_map = extract_all_protocols()
_all_attributes = [format_attr_name(protocol_name + "." + field)
               for protocol_name, protocol_type in _protocol_map.iteritems()
               for field in protocol_type['fields']]


def extract_attr(packet, attr):
    attr_string, converter = extract_attr_converter(attr)
    parts = attr_string.split('.')
    if not parts or len(parts) != 2:
        raise Exception("属性应格式为protocol.attribute")

    protocol_name, attr_name = parts
    protocol_name = protocol_name.lower()
    protocol = _protocol_map.get(protocol_name, None)
    if not protocol:
        raise Exception("位置协议" + protocol_name)

    if attr_name not in protocol['fields']:
        raise Exception("协议" + protocol_name + "不支持属性" + attr_name)

    protocol_class = protocol['class']
    if protocol_class not in packet:
        return None

    raw_attr = getattr(packet[protocol_class], attr_name)
    return converter(raw_attr)


def extract_attributes(pcap_file, attr_list, filter_attributes=None, filter_=None):
    packets_reader = PcapReader(pcap_file)

    try:
        attr_name_list = map(format_attr_name, attr_list)
        while 1:
            packet = packets_reader.read_packet()
            if not packet:
                break

            attributes = dict()
            for i, attr in enumerate(attr_list):
                attributes[attr_name_list[i]] = extract_attr(packet, attr)

            ok = True
            if filter_attributes:
                for filter_attr in filter_attributes:
                    if isinstance(filter_attr, types.StringTypes):
                        filter_attr = format_attr_name(filter_attr)
                        if filter_attr not in attributes or not attributes[filter_attr]:
                            ok = False
                            break

            if ok and filter_:
                ok = filter_(attributes)

            if ok:
                yield attributes
    finally:
        packets_reader.close()


def db_name(pcap_file):
    return


if __name__ == '__main__':
    import pprint

    for attr in extract_attributes("../data/LLS_DDOS_2.0.2-outside.dump", [
        'ether.dst'
    ], filter_attributes=[
        'ether.dst'
    ]):
        print attr
