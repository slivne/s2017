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
    v10 blob,
    v11 blob,
    v12 blob,
    v13 blob,
    v14 blob,
    v15 blob,
    v16 blob,
    v17 blob,
    v18 blob,
    v19 blob,
    PRIMARY KEY (pk, ck)
);
