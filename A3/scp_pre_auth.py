from subprocess import call, PIPE, Popen, check_output
from daemon import *

import os
import socket
import getpass


def main():
    try:
        # for host in ALL_HOSTS:
        #     if host is socket.gethostname() + '.us-west-1.compute.internal':
        #         continue
        pre = 'ubuntu@' + host
        p = Popen(['scp', '-i', '/home/ubuntu/CPEN533.pem', '/home/ubuntu/scp.txt',
                   pre + ':' + '/home/ubuntu/scp.txt'], stdin=PIPE, stdout=PIPE, universal_newlines=True)
        p.stdin.write('yes\n')
    except Exception as e:
        print(e.message)


if __name__ == '__main__':
    main()
