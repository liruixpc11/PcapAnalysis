# coding=UTF-8


from cassandra.cluster import Cluster


cluster = Cluster(['172.16.179.128'])
session = cluster.connect("demo")
rows = session.execute("select * from users")
for row in rows:
    print row.first_name