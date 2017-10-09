#!/bin/python
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel

cluster = Cluster(["127.0.0.1"])
cluster.protocol_version=3
session = cluster.connect()
session.default_consistency_level = ConsistencyLevel.LOCAL_QUORUM
sl = list(session.execute("select sum(ck) from scylla_bench.test where pk=3;"))
print sl

