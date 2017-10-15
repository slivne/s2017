#!/usr/bin/python
import subprocess


#clustering_row_count = 5*100000
partition_count = 1000000
clustering_row_count = 20*100000
clustering_row_size = 10



def run_commands(commands):
    for command in commands: 
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()


def setup():
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
#    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --vnodes -n 1 --version 3.11.0","ccm start --wait-for-binary-proto", command_write, "ccm flush", "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_commands)

def setup_service():
    ccm_commands = ["sudo service syclla-server stop","sudo pkill -9 scylla","sudo rm -Rf /var/lib/scylla/data/*", "sudo rm -Rf /var/lib/scylla/commitlog/*","sleep 3","sudo service scylla-server start","sleep 60"]
#    ccm_commands = ["sudo pkill -9 scylla","sudo pkill -9 java","sudo rm -Rf /var/lib/scylla/cassandra/data/*", "sudo rm -Rf /var/lib/scylla//cassandra/commitlog/*","sudo rm -Rf /var/lib/scylla//cassandra/saved_caches/*","sleep 3","cd ~/cassandra/apache-cassandra-3.11.0/; bin/cassandra","sleep 60"]
    run_commands(ccm_commands)

def stop_start():
    ccm_stop_start_commands = [ "ccm stop", "ccm start --wait-for-binary-proto"]
    run_commands(ccm_stop_start_commands)

def stop_start_service():
    ccm_stop_start_commands = [ "sudo service scylla-server stop", "sudo pkill -9 scylla", "sudo service scylla-server start", "sleep 60"]
    run_commands(ccm_stop_start_commands)


def run_a_test(column_count,write_command,read_command,max_reqs):
    print "column_count %d , write_command %s, read_command %s  max_reqs %d" % (column_count,write_command,read_command,max_reqs)
    command = "-partition-count %d -clustering-row-count 1 -clustering-row-size 10  -clustering-column-count %d --nodes 127.0.0.1" % (partition_count,column_count)
    command_write = "scylla-bench -workload sequential -mode %s %s" % (write_command,command)
    command_read = "scylla-bench -workload uniform -duration 120s -mode %s %s " % (read_command,command)
    if max_reqs > 0:
       command_write = "%s -max-rate %d" % (command_write, max_reqs)
       command_read = "%s -max-rate %d" % (command_read, max_reqs)
    for c in [command_write, command_read]:
        print c
        p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
               print line
        p.wait()


def run_test(schema_prefix,write_command,limit):
    print "run_test_limit %d" % limit

    for column_count in [10,20,30,40,50]:
        schema = "%s_%d.cql" % (schema_prefix, column_count)
        setup_service()
        run_commands(["cqlsh -f %s" % schema])
        run_a_test(column_count,write_command,"read",limit)


run_test("udt","writeUDT",-1)
run_test("regular","write",-1)

run_test("udt","writeUDT",8000)
run_test("regular","write",8000)

