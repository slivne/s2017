CREATE keyspace scylla_bench WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE scylla_bench.test (
    pk bigint,
    ck bigint,
    v00 blob,
    v01 blob,
    v02 blob,
    v03 blob,
    v04 blob,
    v05 blob,
    v06 blob,
    v07 blob,
    v08 blob,
    v09 blob,
    PRIMARY KEY (pk, ck)
);
