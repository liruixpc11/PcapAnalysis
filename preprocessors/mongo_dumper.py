# coding=UTF-8
import datetime

import pymongo
from dumper import Dumper


class MongoDumper(Dumper):
    def __init__(self, path_or_url):
        Dumper.__init__(self, path_or_url, None)
        self.client = None

    def init(self):
        self.client = pymongo.MongoClient(self.path_or_url)

    def close(self):
        self.client.close()

    def save_packet(self, packet_attributes):
        self.client.analysis[self.collection_name].insert_one(packet_attributes)


