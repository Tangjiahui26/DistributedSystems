import os
import sys

virtual_machine_list = ["ubuntu@ec2-54-193-91-241.us-west-1.compute.amazonaws.com",
                        "ubuntu@ec2-13-57-234-1.us-west-1.compute.amazonaws.com",
                        "ubuntu@ec2-13-57-238-30.us-west-1.compute.amazonaws.com",
                        "ubuntu@ec2-54-193-37-145.us-west-1.compute.amazonaws.com",
                        "ubuntu@ec2-54-193-77-234.us-west-1.compute.amazonaws.com",
                        "ubuntu@ec2-54-219-130-46.us-west-1.compute.amazonaws.com"]

def start(hostname):
    key = r"C:\Users\tangj\Desktop\CPEN533\CPEN533.pem"
    cmd = r'"sudo pkill daemon; rm -f ./server*.log; nohup ./A2/GroupMembership/daemon start > /dev/null 2>&1 & " '
    print(cmd)
    # os.system("ssh -i %s %s -o StrictHostKeyChecking=no" % (key, hostname))
    os.system("ssh -i %s %s -o StrictHostKeyChecking=no %s" % (key, hostname, cmd))

def start_virtual_machine(s, e):
    new_list = virtual_machine_list[s-1:e]
    for host in new_list:
        start(host)

if (len(sys.argv) == 3):
    start_virtual_machine((int(sys.argv[1])), int(sys.argv[2]))
else:
    start_virtual_machine(1, 6)