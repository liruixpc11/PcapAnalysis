# coding=UTF-8

from preprocessors import SilkExtractor, SqliteDumper

attr_list = [
    'bytes',
    'sip',
    'sport',
    'dip',
    'dport'
]

max_count = 100
with SqliteDumper("result/silk.sqlite.db", attr_list) as dumper:
    extractor = SilkExtractor()
    count = 0
    for record in extractor.extract('data/LLS_DDOS_2.0.2-outside.rwf', attr_list):
        print record
        dumper.save_packet(record)
        count += 1
        if count > max_count:
            break
