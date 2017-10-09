#!/usr/bin/python
import subprocess


clustering_row_count = 5*1000
clustering_row_size = 10
ks = " create KEYSPACE scylla_bench WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
tb_timeseries_no_static = "CREATE TABLE scylla_bench.test ( pk bigint, ck bigint, v blob, PRIMARY KEY (pk, ck) ) WITH gc_grace_seconds = 600 AND default_time_to_live = 600  AND compaction = {'compaction_window_size': '1',  'compaction_window_unit': 'MINUTES', 'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy'};" 
tb_timeseries_with_static = "CREATE TABLE scylla_bench.test ( pk bigint, ck bigint, s1 blob static, v blob, PRIMARY KEY (pk, ck) ) WITH gc_grace_seconds = 600 AND default_time_to_live = 600  AND compaction = {'compaction_window_size': '1',  'compaction_window_unit': 'MINUTES', 'class': 'org.apache.cassandra.db.compaction.TimeWindowCompactionStrategy'};" 

def run_test(tb):
    command_write = "scylla-bench -workload sequential -mode write -partition-count 1 -max-rate 1000 -clustering-row-count %d -clustering-row-size %d  -use-existing-schema -concurrency 1  -nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", "ccm node1 cqlsh -e \""  + ks +"\"", "ccm node1 cqlsh -e \"" + tb + "\"", command_write, "ccm flush", "sleep 60",  command_write, "ccm flush", "sleep 60",  command_write, "ccm flush","sleep 60",   command_write, "ccm flush", "sleep 60",  command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
#    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 3.11.0","ccm start --wait-for-binary-proto", "ccm node1 cqlsh -e \""  + ks +"\"", "ccm node1 cqlsh -e \"" + tb + "\"", command_write, "ccm flush", "sleep 60",  command_write, "ccm flush", "sleep 60",  command_write, "ccm flush","sleep 60",   command_write, "ccm flush", "sleep 60",  command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
    for command in ccm_commands:
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    command_read = "scylla-bench -workload sequential -mode read -partition-count 1 -clustering-row-count %d -clustering-row-size %d  -concurrency 1 -rows-per-request 1  --nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
           print line
    p.wait()
    
print "no static"
run_test(tb_timeseries_no_static)

print "with static"
run_test(tb_timeseries_with_static)
