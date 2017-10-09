#!/usr/bin/python
import subprocess

ks = " create KEYSPACE ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
tb = "CREATE TABLE ks.tb ( key bigint, val blob, PRIMARY KEY (key) );"

def run_commands(commands):
    for command in commands:
        print command
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def run_test():
    ccm_commands = ["ccm stop","ccm remove scylla-3","ccm create scylla-3 --scylla --vnodes -n 3 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", "ccm node1 cqlsh -e \""+ks+"\"", "ccm node1 cqlsh -e \"" + tb + "\""]
    run_commands(ccm_commands)
    for key in [1,2,3,4,5,6,7,8,9,10]:
        run_commands(["ccm node1 cqlsh -e \"insert into ks.tb (key,val) values (%d,0x00)\"" % key])

    command_read = 'ccm node1 cqlsh -e "tracing on; select * from ks.tb where key in (1,2)"' 
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
           print line
    p.wait()
    
run_test();
