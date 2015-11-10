#!/usr/bin/python
# coding=UTF-8

import pcapy
import pprint
from impacket import ImpactDecoder
from impacket.ImpactPacket import ImpactPacketException
from collections import defaultdict

DMZ_PCAP = "/Users/lirui/datasets/LLDOS/LLS_DDOS_1.0-dmz.dump"


dmz = pcapy.open_offline(DMZ_PCAP)
ip_count_map = defaultdict(lambda: 0)
protocol_type_dict = {
    2048: 'IP',
    2054: 'ARP'
}

eth_decoder = ImpactDecoder.EthDecoder()

while 1:
    try:
        d = dmz.next()
    except pcapy.PcapError:
        break

    if not d:
        break

    header, packet_string = d
    try:
        eth = eth_decoder.decode(packet_string)
        protocol_type = protocol_type_dict.get(eth.get_ether_type(), "<unknown:" + str(eth.get_ether_type()) + ">")
        if protocol_type == 'IP':
            packet = ImpactDecoder.IPDecoder().decode(packet_string)
            ip_count_map[packet.get_ip_src()] += 1
    except ImpactPacketException as ex:
        print 'error: ' + str(ex) + " " + str(len(packet_string))

pprint.pprint(ip_count_map.items())
