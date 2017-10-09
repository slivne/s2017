#!/usr/bin/python
import subprocess


clustering_row_count = 5*100000
clustering_row_size = 10

def run_commands(commands):
    for command in commands: 
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def setup():
    command_write = "scylla-bench -workload sequential -mode write -partition-count 1 -max-rate 1000 -clustering-row-count %d -clustering-row-size %d  -concurrency 1  -nodes 127.0.0.1" % (clustering_row_count, clustering_row_size)
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
#    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 3.11.0","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_commands)

def stop_start():
    ccm_stop_start_commands = [ "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_stop_start_commands)

def run_test():
    setup()

    for rows_per_request in [500,1000]:
        stop_start()
        print rows_per_request
        concurrency = 1000/rows_per_request
        command_read = "scylla-bench -workload uniform -duration 5s -mode read -partition-count 1 -clustering-row-count %d -clustering-row-size %d  -concurrency %d -in-restriction -rows-per-request %d --nodes 127.0.0.1" % (clustering_row_count, clustering_row_size,concurrency,rows_per_request)
        p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
               print line
        p.wait()

    

run_test()
