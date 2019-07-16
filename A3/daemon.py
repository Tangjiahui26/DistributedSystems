import os
import socket
import threading
import datetime
import time
import random
import logging
import json
import collections

# udp socket port number
PORT_NUMBER = 53313

# udp socket port number for file system
PORT_NUMBER_FILE = 53314

TIME_FORMAT = '%b %d %Y %H:%M:%S'

DROP_RATE = 0

# gateway node (introducer node)
INTRODUCER_HOST = 'ip-172-31-0-4.us-west-1.compute.internal'

ALL_HOSTS = [
    'ip-172-31-0-4.us-west-1.compute.internal',   # VM1
    'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
    'ip-172-31-12-166.us-west-1.compute.internal',   # VM3
    'ip-172-31-15-194.us-west-1.compute.internal',  # VM4
    'ip-172-31-26-30.us-west-1.compute.internal',   # VM5
    'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
    # 'ip-172-31-15-194.us-west-1.compute.internal',  # VM7
    # 'ip-172-31-2-22.us-west-1.compute.internal', # VM8
    # 'ip-172-31-0-4.us-west-1.compute.internal', # VM9
    # 'ip-172-31-12-166.us-west-1.compute.internal', # VM10
]

INITIAL_CONTACT_LIST = {
    # VM1
    'ip-172-31-0-4.us-west-1.compute.internal': [
        'ip-172-31-26-30.us-west-1.compute.internal',   # VM5
        'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
        'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
        'ip-172-31-12-166.us-west-1.compute.internal',  # VM3
    ],
    # VM2
    'ip-172-31-31-155.us-west-1.compute.internal': [
        'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
        'ip-172-31-0-4.us-west-1.compute.internal',  # VM1
        'ip-172-31-12-166.us-west-1.compute.internal',  # VM3
        'ip-172-31-15-194.us-west-1.compute.internal',  # VM4
    ],
    # VM3
    'ip-172-31-12-166.us-west-1.compute.internal': [
        'ip-172-31-0-4.us-west-1.compute.internal',  # VM1
        'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
        'ip-172-31-15-194.us-west-1.compute.internal',  # VM4
        'ip-172-31-26-30.us-west-1.compute.internal',  # VM5
    ],
    # VM4
    'ip-172-31-15-194.us-west-1.compute.internal': [
        'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
        'ip-172-31-12-166.us-west-1.compute.internal',  # VM3
        'ip-172-31-26-30.us-west-1.compute.internal',  # VM5
        'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
    ],
    # VM5
    'ip-172-31-26-30.us-west-1.compute.internal': [
        'ip-172-31-12-166.us-west-1.compute.internal',  # VM3
        'ip-172-31-15-194.us-west-1.compute.internal',  # VM4
        'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
        'ip-172-31-0-4.us-west-1.compute.internal',  # VM1
    ],
    # VM6
    'ip-172-31-30-251.us-west-1.compute.internal': [
        'ip-172-31-15-194.us-west-1.compute.internal',  # VM4
        'ip-172-31-26-30.us-west-1.compute.internal',  # VM5
        'ip-172-31-0-4.us-west-1.compute.internal',  # VM1
        'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
    ],
    # # VM7
    # 'ip-172-31-15-194.us-west-1.compute.internal': [
    #     'ip-172-31-26-30.us-west-1.compute.internal', # VM5
    #     'ip-172-31-30-251.us-west-1.compute.internal', # VM6
    #     'ip-172-31-2-22.us-west-1.compute.internal', # VM8
    #     'ip-172-31-0-4.us-west-1.compute.internal', # VM9
    # ],
    # # VM8
    # 'ip-172-31-2-22.us-west-1.compute.internal': [
    #     'ip-172-31-30-251.us-west-1.compute.internal',  # VM6
    #     'ip-172-31-15-194.us-west-1.compute.internal',  # VM7
    #     'ip-172-31-0-4.us-west-1.compute.internal', # VM9
    #     'ip-172-31-12-166.us-west-1.compute.internal', # VM10
    # ], 
    # # VM9
    # 'ip-172-31-12-166.us-west-1.compute.internal': [
    #     'ip-172-31-15-194.us-west-1.compute.internal',  # VM7
    #     'ip-172-31-2-22.us-west-1.compute.internal', # VM8
    #     'ip-172-31-12-166.us-west-1.compute.internal', # VM10
    #     'ip-172-31-0-4.us-west-1.compute.internal',   # VM1
    # ],
    # # VM10
    # 'ip-172-31-12-166.us-west-1.compute.internal': [
    #     'ip-172-31-2-22.us-west-1.compute.internal', # VM8
    #     'ip-172-31-0-4.us-west-1.compute.internal', # VM9
    #     'ip-172-31-0-4.us-west-1.compute.internal',   # VM1
    #     'ip-172-31-31-155.us-west-1.compute.internal',  # VM2
    # ]
}


class MessageType:
    HEARTBEAT = 'HEARTBEAT'
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'
    ACK = 'ACK'

class VMStatus:
    JOINING = 'JOINING'
    RUNNING = 'RUNNING'
    LEAVED = 'LEAVED'
    FAILED = 'FAILED'


class MessageField:
    TYPE = 'type'
    HOST = 'host'
    PORT = 'port'
    CONTENT = 'content'


# def get_current_time():
#     return datetime.datetime.now().strftime(TIME_FORMAT)


class MembershipList:
    def __init__(self, hostname, _id):
        self.details = {
            hostname :{
                'id': _id,
                'status': VMStatus.LEAVED,
                'timestamp': datetime.datetime.now().strftime(TIME_FORMAT)
            }
        }
        # self.details = collections.OrderedDict(sorted(det.items()))


class Daemon:
    def __init__(self, hostname, port, log_file = None):
        self.id = random.randint(0, 65535)
        self.host = hostname + '.us-west-1.compute.internal'
        self.port = port
        self.address = (hostname, self.port)

        # membership list
        self.membership_list = MembershipList(self.host, self.id)
        self.membership_lock = threading.Lock()

        # timeout
        self.timeout_lock = threading.Lock()
        self.timer = {}

        # neighbour list
        self.contact_list = INITIAL_CONTACT_LIST[self.host]
        self.contact_list_lock = threading.Lock()

        # log files
        if log_file:
            self.log_file_name = log_file
        else:
            self.log_file_name = os.getcwd() + '/Server-' + hostname + ".log"

        # sent set() used in file system
        self.sent = set() 


    def print_membership_list(self):        
        self.log("============")
        self.log("MembershipList on %s" % self.host)
        for k, v in self.membership_list.details.items():
            self.log("%s: %d [%s]" % (k, v['id'], v['timestamp']))
        self.log("============")

    def print_contact_list(self):
        self.log("!============!", pr=False)
        self.log("ContactList on %s" % self.host, pr=False)
        for n, node in enumerate(self.contact_list):
            self.log("%d: %s" % (n, node), pr=False)
        self.log("!============!", pr=False)

    def is_introducer(self):
        return self.host == INTRODUCER_HOST

    def log(self, text, pr=True):
        logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG,
                            format='%(asctime)s.%(msecs)04d %(message)s',
                            datefmt=TIME_FORMAT)
        logging.info(text)
        if pr:
            print(text)

    # def update_contact_list(self):
    #     # Create a sorted membership list
    #     det = self.membership_list.details
    #     self.membership_list.details = collections.OrderedDict(sorted(det.items()))

    #     self.contact_list_lock.acquire()
    #     try:
    #         index = list(self.membership_list.details.keys()).index(self.host)
    #     except ValueError:
    #         return -1

    #     if len(self.membership_list.details) == 1:
    #         self.contact_list = INITIAL_CONTACT_LIST[self.host]
    #     elif len(self.membership_list.details) in [2, 3, 4]:
    #         list_mem = list(self.membership_list.details.keys())
    #         list_mem.remove(self.host)
    #         self.contact_list = list_mem
    #     else:
    #         l = len(self.membership_list.details)
    #         self.contact_list = [
    #             list(self.membership_list.details.keys())[index - 2],
    #             list(self.membership_list.details.keys())[index - 1],
    #             list(self.membership_list.details.keys())[(index + 1) % l],
    #             list(self.membership_list.details.keys())[(index + 2) % l],
    #         ]
    #     self.contact_list_lock.release()

    def heartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                # send heartbeat message every 0.5 second
                time.sleep(0.5)

                # messages are lost with different probabilities
                if random.random() < DROP_RATE:
                    continue
                else:

                    if self.membership_list.details[self.host]['status'] == VMStatus.LEAVED:
                        continue

                    # self.print_membership_list()
                    # self.print_contact_list()
                    
                    current = datetime.datetime.now()
                    self.membership_lock.acquire()
                    self.membership_list.details[self.host]['status'] == VMStatus.RUNNING
                    self.membership_list.details[self.host]['timestamp'] = current.strftime(TIME_FORMAT)

                    for host in self.contact_list:
                        if host not in self.membership_list.details:
                            continue
                        heartbeat_message = {
                            MessageField.TYPE: MessageType.HEARTBEAT,
                            MessageField.HOST: self.host,
                            MessageField.PORT: self.port,
                            MessageField.CONTENT: self.membership_list.details
                        }
                        sock.sendto(json.dumps(heartbeat_message).encode('utf-8'), (host, self.port))

                        # save the send time for the timeout checking
                        self.timeout_lock.acquire()
                        if host in self.membership_list.details and host not in self.timer:
                            self.timer[host] = datetime.datetime.now()
                        self.timeout_lock.release()

                    # self.update_contact_list()
                    self.membership_lock.release()

            except Exception as e:
                print(e.message)
                self.log(e.message)

    def timeout(self):
        timer = self.timer
        while True:
            try:
                # self.timeout_lock.acquire()
                for host in list(timer.keys()):
                    now = datetime.datetime.now()
                    time_diff = now - timer.get(host, datetime.datetime.now())
                    # timeout after two seconds
                    if time_diff.days >= 0 and time_diff.seconds > 2.:
                        if (host in self.membership_list.details) and \
                           (self.membership_list.details[host]['status'] not in {VMStatus.FAILED, VMStatus.LEAVED}):
                            self.log("Timeout for host %s." % host)

                            # self.membership_lock.acquire()
                            # del self.membership_list.details[host]
                            # self.update_contact_list()
                            # self.membership_lock.release()

                            self.membership_list.details[host]['status'] = VMStatus.FAILED
                            self.membership_list.details[host]['timestamp'] = now.strftime(TIME_FORMAT)

                        try:
                            del timer[host]
                        except Exception as e:
                            print(e.message)
                            self.log(e.message)
                            pass
                # self.timeout_lock.release()

                for host in list(self.membership_list.details.keys()):
                    if host in self.membership_list.details:
                        timestamp = datetime.datetime.strptime(self.membership_list.details[host]['timestamp'], TIME_FORMAT)
                        current = datetime.datetime.now()
                        diff = current - timestamp
                        if self.membership_list.details[host]['status'] == VMStatus.FAILED \
                            and diff.days >= 0 and diff.seconds > 3. and (host not in self.sent):
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            failed_message = {
                                'type': 'failed_relay',
                                'host': host,
                            }
                            sock.sendto(json.dumps(failed_message).encode('utf-8'), (self.host, PORT_NUMBER_FILE))
            except Exception as e:
                print(e.message)
                self.log(e.message)
                pass

    def join(self):
        # send join request to the introducer
        if self.is_introducer():
           self.log("host %s is introducer" % self.host)

        self.membership_list.details[self.host]['status'] = VMStatus.RUNNING
        self.membership_list.details[self.host]['timestamp'] = datetime.datetime.now().strftime(TIME_FORMAT)
        self.membership_list.details[self.host]['id'] = random.randint(0, 65535)

        if not self.is_introducer():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.log("Send join message to introducer")
            join_message = {
                MessageField.TYPE: MessageType.JOIN,
                MessageField.HOST: self.host,
                MessageField.PORT: self.port,
                MessageField.CONTENT: self.membership_list.details[self.host]
            }
            sock.sendto(json.dumps(join_message).encode('utf-8'), (INTRODUCER_HOST, PORT_NUMBER))

    def leave(self):
        # send leave message to contacts
        if self.membership_list.details[self.host]['status'] != VMStatus.RUNNING:
            self.log("Cannot leave if the host %s is not in the membership list" % self.host)
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log("Send leave message to contacts")
        leave_message = {
            MessageField.TYPE: MessageType.LEAVE,
            MessageField.HOST: self.host,
            MessageField.PORT: self.port,
        }
        for host in self.contact_list:
            sock.sendto(json.dumps(leave_message).encode('utf-8'), (host, PORT_NUMBER))

        # self.membership_lock.acquire()
        # self.membership_list.details.clear()
        # self.membership_list = MembershipList(self.host, self.id)
        # self.update_contact_list()
        # self.membership_lock.release()
        self.membership_list.details[self.host]['status'] = VMStatus.LEAVED

        self.log('Host %s leaves the group' % self.host)

    def receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.address)
        while True:
            try:
                if self.membership_list.details[self.host]['status'] == VMStatus.LEAVED:
                    continue

                data, addr = sock.recvfrom(4096)
                if data:
                    message = json.loads(data.decode('utf-8'))
                    message_type = message.get(MessageField.TYPE, '#')
                    if message_type == '#':
                        self.log('Undefined Type')
                        continue
                    self.log('Receive %s message from %s:%s' % (message[MessageField.TYPE],
                                                             message[MessageField.HOST],
                                                             message[MessageField.PORT]), False)
                    send_host = message[MessageField.HOST]
                    current_time = datetime.datetime.now().strftime(TIME_FORMAT)

                    self.membership_lock.acquire()

                    # HEARTBEAT message 
                    if message_type == MessageType.HEARTBEAT:
                        content = message[MessageField.CONTENT]
                        for host in content:
                            if host not in self.membership_list.details:
                                self.membership_list.details[host] = content[host]
                                continue
                            time_saved = datetime.datetime.strptime(self.membership_list.details[host]['timestamp'],
                                                                    TIME_FORMAT)
                            time_received = datetime.datetime.strptime(content[host]['timestamp'],
                                                                       TIME_FORMAT)
                            # update when the timestamp is newer
                            if time_received > time_saved:
                                self.membership_list.details[host] = content[host]

                            ack_message = {
                                MessageField.TYPE: MessageType.ACK,
                                MessageField.HOST: self.host,
                                MessageField.PORT: PORT_NUMBER,
                                MessageField.CONTENT: self.membership_list.details[self.host]
                            }
                            sock.sendto(json.dumps(ack_message).encode('utf-8'), (send_host, PORT_NUMBER))

                    # ACK message 
                    elif message_type == MessageType.ACK:
                        self.membership_list.details[send_host] = message[MessageField.CONTENT]
                        if send_host in self.timer:
                            self.timeout_lock.acquire()
                            del self.timer[send_host]
                            self.timeout_lock.release()

                    # Join message 
                    elif message_type == MessageType.JOIN:
                        self.membership_list.details[send_host] = message[MessageField.CONTENT]
                        self.membership_list.details[send_host]['status'] == VMStatus.JOINING
                        self.membership_list.details[send_host]['timestamp'] = current_time
                        self.sent.discard(send_host)
                        if self.is_introducer():
                            # if it is introducer, then
                            # multicast to contact lists
                            # about the JOIN
                            sock_new = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            join_message = {
                                MessageField.TYPE: MessageType.JOIN,
                                MessageField.HOST: send_host,
                                MessageField.PORT: PORT_NUMBER,
                                MessageField.CONTENT: self.membership_list.details[send_host]
                            }
                            for host in ALL_HOSTS:
                                if host != send_host and host != self.host:
                                    sock_new.sendto(json.dumps(join_message).encode('utf-8'), (host, PORT_NUMBER))
                            
                            # send message to file system program
                            sock_file = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            join_message_file = {
                                'type': 'join',
                                'host': [send_host],
                            }
                            sock_file.sendto(json.dumps(join_message_file).encode('utf-8'), (self.host, PORT_NUMBER_FILE))

                    elif message_type == MessageType.LEAVE:
                        # LEAVE message
                        self.membership_list.details[send_host]['status'] = VMStatus.LEAVED
                        self.membership_list.details[send_host]['timestamp'] = current_time
                        # if send_host in self.membership_list.details:
                        #     del self.membership_list.details[send_host]
                        #     self.update_contact_list()

                    else:
                        self.log('UNKNOWN TYPE OF MESSAGE RECEIVED')

                    self.membership_lock.release()
            except Exception as e:
                self.log(e.message)

    def commands(self):
        commands_list = '''
        ===== Command Lists =====
        ---> join: Join the group.
        ---> leave: Leave the group.
        ---> ml: Print membership List
        ---> id: Print current id of the server
        '''
        print(commands_list)
        while True:
            arg = input('--->')
            if arg == 'join':
                self.join()
            elif arg == 'leave':
                self.leave()
            elif arg == 'ml':
                self.print_membership_list()
            elif arg == 'id':
                print(self.id)
            else:
                self.log('UNKNOW ARGUMENT %s' % arg)

    def run(self):
        receiver_t = threading.Thread(target=self.receiver)
        heartbeat_t = threading.Thread(target=self.heartbeat)
        timeout_t = threading.Thread(target=self.timeout)
        # commands_t = threading.Thread(target=self.commands)

        receiver_t.start()
        heartbeat_t.start()
        timeout_t.start()
        # commands_t.start()
        # receiver_t.join()
        # heartbeat_t.join()
        # timeout_t.join()
        # commands_t.join()


def main():
    server = Daemon(hostname=socket.gethostname(), port=PORT_NUMBER)
    server.run()


if __name__ == '__main__':
    main()
