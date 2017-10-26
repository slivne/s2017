#!/usr/bin/python
import subprocess

def cp_file(server,file):
    command_to_run = "scp -i a.pem %s centos@%s:" % (file,server)
    print command_to_run
    p = subprocess.Popen(command_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()

def run_commands(server,commands):
    for command in commands: 
        command_to_run = "ssh -i a.pem centos@%s \'%s\'" % (server,command)
        print command
        p = subprocess.Popen(command_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()


loaders = ["52.55.254.55","54.210.141.188","52.90.201.53","54.242.42.44","54.88.178.121","54.89.121.29","34.204.96.210","34.226.200.23","52.207.231.116","34.201.218.200","34.207.102.87","54.91.236.198","54.173.227.166"]


for loader in loaders:
    cp_file(loader,"run_cassandra_stress.sh")
    run_commands(loader,['pkill -9 java ; pkill -9 run_cassandra ; nohup /home/centos/run_cassandra_stress.sh 0 1 >& out &'])

