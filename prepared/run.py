#!/usr/bin/python
import subprocess


def run_test():
    ccm_commands = ["ccm stop","ccm remove scylla-1","ccm create scylla-1 --scylla --vnodes -n 1 --install-dir=/home/shlomi/scylla","ccm start --wait-for-binary-proto", "ccm node1 stress write n=100000", "ccm nide1 stress read n=100000"]
    for ccm_command in ccm_commands:
        p = subprocess.Popen(ccm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    print "unprepared"
    command_read = "ccm node1 stress read n=100000 -mode native unprepared cql3 -rate threads=20" 
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
           print line
    p.wait()
    
    print "prepared"
    command_read = "ccm node1 stress read n=100000 -mode native cql3 -rate threads=20" 
    p = subprocess.Popen(command_read, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
           print line
    p.wait()
    
run_test();
