# coding=UTF-8
import uuid
import datetime

from preprocessors import SqliteDumper, PcapExtractor, MongoDumper


attr_list = [
    'ether.dst'
]
count = 2000
with SqliteDumper("result/pcap.sqlite.db", attr_list) as dumper:
# with MongoDumper('mongodb://172.16.179.128:27017/') as dumper:
    for packet_attributes in PcapExtractor().extract("data/LLS_DDOS_2.0.2-outside.dump", attr_list,
                                                     filter_attributes=[
                                                         'ether_dst'
                                                     ]):
        count -= 1
        dumper.save_packet(packet_attributes)
        if count <= 0:
            break


