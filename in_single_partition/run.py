#!/usr/bin/python
import subprocess


partition_count = 100
clustering_row_count = 10*10000
#clustering_row_count = 20*1000
clustering_row_size = 100

def run_commands(commands):
    for command in commands: 
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

command_write = "scylla-bench -workload sequential -mode write -partition-count 1 -clustering-row-count %d -clustering-row-size %d  -concurrency 4  -nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)

def setup():
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
#    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 3.11.0","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_commands)

def setup_service():
    ccm_commands = ["sudo service syclla-server stop","sudo pkill -9 scylla","sudo rm -Rf /var/lib/scylla/data/*", "sudo rm -Rf /var/lib/scylla/commitlog/*","sleep 3","sudo service scylla-server start","sleep 60", command_write, "nodetool flush"]
    ccm_commands = ["sudo service syclla-server stop","sudo pkill -9 scylla","sudo rm -Rf /var/lib/scylla/data/*", "sudo rm -Rf /var/lib/scylla/commitlog/*","sleep 3","sudo service scylla-server start","sleep 60"]
#    ccm_commands = ["sudo pkill -9 scylla","sudo pkill -9 java","sudo rm -Rf /var/lib/scylla/cassandra/data/*", "sudo rm -Rf /var/lib/scylla//cassandra/commitlog/*","sudo rm -Rf /var/lib/scylla//cassandra/saved_caches/*","sleep 3","cd ~/cassandra/apache-cassandra-3.11.0/; bin/cassandra","sleep 60"]
    
    run_commands(ccm_commands)
    for partition in range(partition_count+1):
        write_partition = "%s -partition-offset %d" % (command_write, partition)
        run_commands([write_partition])
    run_commands(["nodetool flush"])

def stop_start():
    ccm_stop_start_commands = [ "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_stop_start_commands)

def stop_start_service():
    ccm_stop_start_commands = [ "sudo service scylla-server stop", "sudo pkill -9 scylla", "sudo service scylla-server start", "sleep 60"]
    run_commands(ccm_stop_start_commands)


def run_a_test(rows_per_request,concurrency,max_reqs):
#    stop_start_service()
    print "rows_per_request %d concurrency %d max_reqs %d" % (rows_per_request,concurrency,max_reqs)
    command_read = "scylla-bench -workload uniform -duration 30s -mode read -partition-count %d -clustering-row-count %d -clustering-row-size %d  -concurrency %d -in-restriction -rows-per-request %d --nodes 127.0.0.1" % (partition_count,clustering_row_count, clustering_row_size,concurrency,rows_per_request)
    if max_reqs > 0:
       command_read = "%s -max-rate %d" % (command_read, max_reqs)
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
           print line
    p.wait()


def run_test_in_query_vs_split_query(limit):
    print "run_test_in_query_vs_split_query limit rows %d" % limit
    setup_service()

    max_reqs = -1
    if limit > 0:
       max_reqs = limit

    for concurrency in [1,2,3,4,5,10,25,50,100]:
        run_a_test(1,concurrency,max_reqs);

    for rows_per_request in [2,3,4,5,10,25,50,100]:
        max_reqs = -1
        if limit > 0:
            max_reqs = limit/rows_per_request
        run_a_test(rows_per_request,1,max_reqs);

def run_test_in_query_limited_concurrency(limit):
    print "run_test_in_query_limited_concurrency limit rows %d" % limit
    setup_service()
 

    for rows_per_request in [1,2,3,4,5,10,25,50,100]:
        max_reqs = -1
        if limit > 0:
            max_reqs = limit/rows_per_request
        run_a_test(rows_per_request,10,max_reqs)


#run_test_in_query_limited_concurrency(2000)
#run_test_in_query_limited_concurrency(-1)

run_test_in_query_vs_split_query(500)
run_test_in_query_vs_split_query(-1)
