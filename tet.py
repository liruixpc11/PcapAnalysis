# coding=UTF-8
import pprint

from preprocessors import PcapExtractor, SilkExtractor


pprint.pprint(list(SilkExtractor().all_attributes()))
