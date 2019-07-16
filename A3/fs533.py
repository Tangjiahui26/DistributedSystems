from subprocess import call, PIPE, Popen, check_output
from signal import signal, alarm, SIGALRM
from glob import *
from pprint import pprint
from daemon import *

import os
import socket
import threading
import datetime
import time
import random
import logging
import json
import collections
import shutil
import hashlib
import select
import sys
import filecmp

# # create a signal ZeroDivisionError for interupt the input
# signal(SIGALRM, lambda x:1/0)

FILE_SYSTEM_PATH = os.path.join(os.path.expanduser('~'), 'fs533')
NODE_NUMBER = 6
# be capable of tolerating two server/machine failures at a time
REPLICAS_NUMBER = 4


def hostname_to_vm_id(hostname):
    vm_id = ALL_HOSTS.index(hostname) + 1
    return vm_id


def vm_id_to_hostname(vm_id):
    return ALL_HOSTS[vm_id - 1]


def message_digest_file(file):
    # use SHA-256 to hash the file name
    message_digest = hashlib.sha256(file.encode()).hexdigest()
    # possible hash result: 1 - NODE_NUMBER
    hash_number = sum(ord(c) for c in message_digest) % NODE_NUMBER + 1
    return hash_number


def get_default_replicas(pid):
    # return four replicas pid
    pid_list = {(pid + i) % NODE_NUMBER + 1 for i in range(REPLICAS_NUMBER)}
    return pid_list


class FileTable:
    def __init__(self):
        self.id_mapper = {i + 1: set() for i in range(NODE_NUMBER)}
        self.file_mapper = {}

    def add_file(self, file_name, vm_ids):
        for i in vm_ids:
            self.id_mapper[i].add(file_name)
        if file_name not in self.file_mapper:
            self.file_mapper[file_name] = {
                'status': '',
                'timestamp': 0,
                'replicas': set(),
            }
        # update file info: 'status' should be wr-able (write-readable)
        self.file_mapper[file_name]['status'] = 'wr-able'
        self.file_mapper[file_name]['timestamp'] = datetime.datetime.now().strftime(TIME_FORMAT)
        self.file_mapper[file_name]['replicas'] |= vm_ids

    def delete_file(self, file_name):
        for i in self.id_mapper:
            self.id_mapper[i].discard(file_name)
        if file_name in self.file_mapper:
            del self.file_mapper[file_name]


class FS533:
    def __init__(self, hostname, port):
        self.host = hostname + '.us-west-1.compute.internal'
        self.port = port
        self.address = (hostname, self.port)
        self.vm_id = hostname_to_vm_id(self.host)
        self.lives = {self.vm_id}

        # log file
        self.log_file_name = os.getcwd() + '/FS533-' + hostname + ".log"

        # create a file table and failure detector (daemon) for each fs533 server
        self.file_table = FileTable()
        self.daemon = Daemon(socket.gethostname(), PORT_NUMBER, log_file=self.log_file_name)

    def log(self, text, pr=True):
        logging.basicConfig(filename=self.log_file_name, level=logging.INFO,
                            format='%(asctime)s.%(msecs)04d %(message)s',
                            datefmt=TIME_FORMAT)
        logging.info(text)
        if pr:
            print(text)

    def put_file(self, local_file_name, fs533_file_name):
        # for the measurements
        time_n = datetime.datetime.now()
        self.log('Start Putting %s into fs533' % fs533_file_name)
        if not os.path.exists(local_file_name):
            self.log('No such file %s' % local_file_name)
            return
        file_mapper = self.file_table.file_mapper
        if fs533_file_name in file_mapper:
            target_ids = file_mapper[fs533_file_name]['replicas']
            file_status = file_mapper[fs533_file_name]['status']
            if file_status != 'wr-able':
                self.log('Other writing operation is not finished. Wait for a monment!')
                return
            init_time = datetime.datetime.strptime(file_mapper[fs533_file_name]['timestamp'], TIME_FORMAT)
            current_time = datetime.datetime.now()
            diff = current_time - init_time
            # Two puts within 1 minutes
            if diff.days >= 0 and diff.seconds <= 60.:
                # try:
                #     alarm(30)
                #     input("Press enter to continue.")
                # except ZeroDivisionError:
                #     print("timed out")
                #     return

                # try:
                #     print('Press enter to continue.')
                #     time.sleep(30)
                # except KeyboardInterrupt:
                #     print("Continue to put the file.")
                # else:
                #     print("time out")
                #     return
                print('Press enter to continue.', end='', flush=True)
                self.log('Press enter to continue.', pr=False)
                r, w, x = select.select([sys.stdin], [], [], 30)
                if not r:
                    print('\ntime out')
                    self.log('\ntime out', pr=False)
                    return
                else:
                    print('\nContinue to put the file.')
                    self.log('\nContinue to put the file.', pr=False)
        else:
            target_ids = get_default_replicas(message_digest_file(local_file_name))

        # update file status to other nodes
        sock_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        status_message = {
            'type': 'status-update',
            'filename': fs533_file_name,
            'status': 'writing'
        }
        for host in ALL_HOSTS:
            sock_status.sendto(json.dumps(status_message).encode('utf-8'), (host, self.port))

        self.log('Put file %s to %s' % (local_file_name, fs533_file_name))
        for i in target_ids:
            target_hostname = vm_id_to_hostname(i)
            pre = 'ubuntu@' + target_hostname
            try:
                p = Popen(['scp', '-i', '/home/ubuntu/CPEN533.pem', local_file_name, pre + ':' + os.path.join(FILE_SYSTEM_PATH, fs533_file_name)], stdout=PIPE)
                p.wait()
            except Exception as e:
                print(e.message)
                self.log(e.message)
        self.file_table.add_file(fs533_file_name, target_ids)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        update_message = {
            'type': 'update',
            'filename': fs533_file_name,
            'replicas': list(target_ids),
            'timestamp': file_mapper[fs533_file_name]['timestamp'],
            'status': file_mapper[fs533_file_name]['status']
        }
        for host in ALL_HOSTS:
            sock.sendto(json.dumps(update_message).encode('utf-8'), (host, self.port))
        # for the measurements
        time_f = datetime.datetime.now()
        time_d = time_f - time_n
        self.log('Finish Putting %s into fs533 using time %s' % (fs533_file_name, str(time_d)))


    def get_file(self, fs533_file_name, local_file_name):
        # for the measurements
        time_n = datetime.datetime.now()
        self.log('Start getting %s from fs533' % fs533_file_name)        
        file_mapper = self.file_table.file_mapper
        if fs533_file_name not in file_mapper:
            self.log('No such file %s in fs533 file system' % fs533_file_name)
            return

        get_file_id = list(file_mapper[fs533_file_name]['replicas'])[0]
        status = file_mapper[fs533_file_name]['status']
        if status != 'wr-able':
            self.log('Other writing operation is not finished. Wait for a monment!')
            return

        pre = 'ubuntu@' + vm_id_to_hostname(get_file_id)
        try:
            p = Popen(['scp', '-i', '/home/ubuntu/CPEN533.pem', pre + ':' + os.path.join(FILE_SYSTEM_PATH, fs533_file_name), local_file_name], stdout=PIPE)
            p.wait()
            self.log('Get file %s from vm_id %s' % (fs533_file_name, get_file_id))
        except Exception as e:
            print(e.message)
            self.log(e.message)
        # for the measurements
        time_f = datetime.datetime.now()
        time_d = time_f - time_n
        self.log('Finish getting %s from fs533 using time %s' % (fs533_file_name, str(time_d)))

    def remove_file(self, fs533_file_name):
        # for the measurements
        time_n = datetime.datetime.now()
        self.log('Start removing %s from fs533' % fs533_file_name) 
        file_mapper = self.file_table.file_mapper
        if fs533_file_name not in file_mapper:
            self.log('No such file %s in fs533 file system' % fs533_file_name)
            return
        status = file_mapper[fs533_file_name]['status']
        if status != 'wr-able':
            self.log('Other writing operation is not finished. Wait for a monment!')
            return

        self.file_table.delete_file(fs533_file_name)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        remove_message = {
            'type': 'remove',
            'filename': fs533_file_name
        }
        for host in ALL_HOSTS:
            sock.sendto(json.dumps(remove_message).encode('utf-8'), (host, self.port))
        # for the measurements
        time_f = datetime.datetime.now()
        time_d = time_f - time_n
        self.log('Finish removing %s from fs533 using time %s' % (fs533_file_name, str(time_d)))

    def ls(self):
        pprint(self.file_table.id_mapper)

    def locate_file(self, fs533_file_name):
        file_mapper = self.file_table.file_mapper
        if fs533_file_name not in file_mapper:
            self.log('No such file %s in fs533 file system' % fs533_file_name)
            return
        pprint(file_mapper[fs533_file_name])

    def ls_here(self):
        for file in os.listdir(FILE_SYSTEM_PATH):
            pprint(file)

    def receiver(self):
        file_mapper = self.file_table.file_mapper
        id_mapper = self.file_table.id_mapper

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.address)

        while True:
            data, addr = sock.recvfrom(4096)
            if data:
                message = json.loads(data.decode('utf-8'))
                message_type = message['type']

                if message_type == 'update':
                    pprint(message)
                    self.log(message, pr=False)
                    self.log('Receive update message')
                    filename = message['filename']
                    replicas = set(message['replicas'])
                    for replica in replicas:
                        id_mapper[replica].add(filename)
                    if filename not in file_mapper:
                        file_mapper[filename] = {
                            'status': '',
                            'timestamp': 0,
                            'replicas': set(),
                        }
                    file_mapper[filename]['status'] = message['status']
                    file_mapper[filename]['timestamp'] = message['timestamp']
                    file_mapper[filename]['replicas'] |= replicas

                elif message_type == 'remove':
                    pprint(message)
                    self.log(message, pr=False)
                    self.log('Receive remove message')
                    filename = message['filename']
                    self.file_table.delete_file(filename)

                    for file in os.listdir(FILE_SYSTEM_PATH):
                        file_path = os.path.join(FILE_SYSTEM_PATH, file)
                        if os.path.isfile(file_path) and file.startswith(filename):
                            self.log('Find and delete file %s' % file)
                            os.remove(file_path)

                elif message_type == 'failed_relay':
                    i = hostname_to_vm_id(message['host'])
                    if i not in self.lives:
                        continue

                    self.log('Receive failed_relay message')
                    self.lives.discard(i)

                    for f in id_mapper[i]:
                        replicas = file_mapper[f]['replicas']
                        replicas.discard(i)

                        # re-update if it is possible
                        try:
                            if self.vm_id == max(replicas):
                                random_id = random.choice(list(self.lives - replicas))
                                for file in os.listdir(FILE_SYSTEM_PATH):
                                    file_path = os.path.join(FILE_SYSTEM_PATH, file)
                                    if os.path.isfile(file_path) and file.startswith(f):
                                        self.log('Re-replica file %s to %d' % (file, random_id))
                                        pre = 'ubuntu@' + vm_id_to_hostname(random_id)
                                        p = Popen(['scp', '-i', '/home/ubuntu/CPEN533.pem', file_path, pre + ':' + file_path], stdout=PIPE)
                                        p.wait()

                                sock_new = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                update_message = {
                                    'type': 'update',
                                    'filename': f,
                                    'replicas': list({random_id} | replicas),
                                    'timestamp': file_mapper[f]['timestamp'],
                                    'status': file_mapper[f]['status']
                                }
                                for host in ALL_HOSTS:
                                    sock_new.sendto(json.dumps(update_message).encode('utf-8'), (host, self.port))
                        except Exception as e:
                            print(e.message)
                            self.log(e.message)
                            pass
                    # TODO remove f in id_mapper eventually?

                elif message_type == 'join':
                    pprint(message)
                    self.log(message, pr=False)
                    self.log('Receive join message')
                    if self.daemon.is_introducer():
                        # multicast join message
                        # update lives
                        # TODO here
                        join_id = hostname_to_vm_id(message['host'][0])
                        self.lives.add(join_id)
                        sock_join = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        join_message = {
                            'type': 'join',
                            'lives': list(self.lives),
                        }
                        for host in ALL_HOSTS:
                            if host != self.host:
                                sock_join.sendto(json.dumps(join_message).encode('utf-8'), (host, self.port))
                    else:
                        self.lives |= set(message['lives'])
                elif message_type == 'status-update':
                    self.log(message)
                    filename = message['filename']
                    if filename not in file_mapper:
                        continue
                    else:
                        file_mapper[filename]['status'] = message['status']

    def test(self):
        # test set-up: generate random local files
        test_folder = os.path.join(os.path.expanduser('~'), 'A3_test')
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)

        os.mkdir(test_folder)            
        num_files = 10
        avail_filenames = set()
        for num in range(num_files):
            avail_filenames.add('random_file-' + str(num))

        try:
            for filename in avail_filenames:
                filepath = os.path.join(test_folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(os.urandom(1024))
                # put operation
                self.put_file(filepath, filename)

            # ls operation
            ls_filenames = set()
            for v in self.file_table.id_mapper.values():
                ls_filenames |= v
            if ls_filenames != avail_filenames:
                print('Test failed! Files in fs533 file system are not as expected.')
                return
            else:
                self.ls()
                print('Put and ls operation passed.')
            # get operation into a different place
            for f in ls_filenames:
                new_localpath = f + '-new'
                self.get_file(f, os.path.join(test_folder, new_localpath))
                if not filecmp.cmp(os.path.join(test_folder, new_localpath), os.path.join(test_folder, f)):
                    print('Test failed! Get returned a file with different contents than the original')
                    return
                else:
                    print('Get operation passed.')
            # remove and ls operation
            for f in ls_filenames:
                self.remove_file(f)
            ls_new_filenames = set()
            for v in self.file_table.id_mapper.values():
                ls_new_filenames |= v
            if len(ls_new_filenames) != 0:
                print('Test failed! Should have no files in fs533 file system')
                return
            else:
                self.ls()
                print('Remove and ls operation passed.')

            print('Tests passed!')
        except Exception as e:
            print(e)

    def commands(self):
        commands_list = '''
        ===== Command Lists =====
        ---> join: Join the group.
        ---> leave: Leave the group.
        ---> ml: Print membership List
        ---> id: Print current id of the server
        ---> put [localfilename] [fs533filename]: add a local file to fs533 with the given fs533 name
        ---> get [fs533filename] [localfilename]:  fetch a fs533 file to the local machine
        ---> remove [fs533filename] : delete a file from fs533
        ---> ls : list all files in fs533
        ---> locate [fs533filename] : list all machines (name / id / IP address) of the servers that contain a copy of the file
        ---> lshere : list all fs533 files stored on the local machine
        ---> test : test the basic operations of fs533 file system
        '''
        print(commands_list)
        while True:
            arg = input('--->')
            args = arg.split(' ')
            if arg == 'join':
                self.daemon.join()
            elif arg == 'ml':
                self.daemon.print_membership_list()
            elif arg == 'leave':
                self.daemon.leave()
            elif arg.startswith('put'):
                if len(args) != 3:
                    print('Format is: put [localfilename] [fs533filename]')
                    continue
                self.put_file(args[1], args[2])
            elif arg.startswith('get'):
                if len(args) != 3:
                    print('Format is: get [fs533filename] [localfilename]')
                    continue
                self.get_file(args[1], args[2])
            elif arg.startswith('remove'):
                if len(args) != 2:
                    print('Format is: remove [fs533filename]')
                    continue
                self.remove_file(args[1])
            elif arg == 'ls':
                self.ls()
            elif arg.startswith('locate'):
                if len(args) != 2:
                    print('Format is: locate [fs533filename]')
                    continue
                self.locate_file(args[1])
            elif arg == 'lshere':
                self.ls_here()
            # TODO add test here
            elif arg == 'test':
                self.test()
            else:
                self.log('UNKNOW ARGUMENT %s' % arg)

    def run(self):
        self.daemon.run()
        if os.path.exists(FILE_SYSTEM_PATH):
            shutil.rmtree(FILE_SYSTEM_PATH)
        os.mkdir(FILE_SYSTEM_PATH)
        command_t = threading.Thread(target=self.commands)
        receiver_t = threading.Thread(target=self.receiver)
        receiver_t.start()
        command_t.start()
        receiver_t.join()
        command_t.join()


def main():
    fs533 = FS533(socket.gethostname(), PORT_NUMBER_FILE)
    fs533.run()


if __name__ == '__main__':
    main()
