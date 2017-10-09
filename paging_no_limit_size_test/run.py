#!/usr/bin/python
import subprocess


def boot_cluster():
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto"]
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 3.11.0","ccm start --wait-for-binary-proto"]
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 2.1.15","ccm start --wait-for-binary-proto"]
    for ccm_command in ccm_commands:
        p = subprocess.Popen(ccm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()


def run_page_size_test(clustering_row_count,clustering_row_size,page_size):
    command_read = "scylla-bench -workload sequential -mode read -partition-count 1 -clustering-row-count %d -clustering-row-size %d  -concurrency 1  -nodes 127.0.0.1 -page-size %d -no-lower-bound -no-cql-limit -protocol-version 3 -no-client-compression -duration 20s" % (clustering_row_count,clustering_row_size,page_size)
#    print command_read
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
       if line.strip().startswith("99th"):
           print "%d %s" % (page_size,line.split(':')[1].strip())
    p.wait()
    
def run_test(clustering_row_count,clustering_row_size):
    print "running test for rows %d size %d" % (clustering_row_count, clustering_row_size)
    command_write = "scylla-bench -workload sequential -mode write -partition-count 1 -protocol-version 3 -clustering-row-count %d -clustering-row-size %d  -concurrency 1  --nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)
    command_read = "scylla-bench -workload sequential -mode read -partition-count 1 -protocol-version 3 -clustering-row-count %d -clustering-row-size %d  -concurrency 1  --nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)
#    print command_write
    p = subprocess.Popen(command_write, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
#    print command_read
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    
    for page_size in [10,50,100,1000,2500,5000,10000,50000]:
       run_page_size_test(clustering_row_count,clustering_row_size,page_size) 


for clustering_row_size in [10,100,1000,10000]:
    boot_cluster()
    run_test(5*1000000/clustering_row_size,clustering_row_size)
#    run_test(1*10000000/clustering_row_size,clustering_row_size)
