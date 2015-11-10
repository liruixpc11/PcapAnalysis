# coding=UTF-8

from cassandra.cluster import Cluster
from dumper import Dumper


class CassandraDumper(Dumper):
    def __init__(self, path_or_url, attr_list, keyspace_name='packets'):
        Dumper.__init__(self, path_or_url, attr_list)
        self.cluster = None
        self.session = None
        self.keyspace_name = keyspace_name

    def init(self):
        self.cluster = Cluster(self.path_or_url)
        self.session = self.cluster.connect()
        self.session.execute("CREATE KEYSAPCE IF NOT EXISTS {0}".format(self.keyspace_name))
        self.session.execute("""CREATE TABLE IF NOT EXISTS {0}.{1}
""".format(self.keyspace_name, self.collection_name,
           ))

    def close(self):
        self.cluster.shutdown()
