#!/bin/python
from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"])
cluster.protocol_version=3
session = cluster.connect()
#session.default_fetch_size=20
session.execute("select * from scylla_bench.test where pk=0;")

