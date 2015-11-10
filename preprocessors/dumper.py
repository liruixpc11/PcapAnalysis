# coding=UTF-8
import datetime


class Dumper:
    def __init__(self, path_or_url, attr_list=None, collection_name=None):
        self.path_or_url = path_or_url
        self.attr_list = attr_list
        self.collection_name = collection_name if collection_name else "D" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def init(self):
        pass

    def save_packet(self, packet_attributes):
        pass

    def close(self):
        pass

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
