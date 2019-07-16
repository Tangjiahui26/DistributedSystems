#ifndef DAEMON_H
#define DAEMON_H

#include <vector>
#include <stdio.h>
#include <algorithm>
#include <map>
#include <thread>
#include <mutex>
#include <ctime>
#include <string>
#include <sys/time.h>
#include <stdarg.h>
#include "udpsocket.h"
#include "virtualmachine.h"

#define DROPRATE 0
#define INTRODUCER 5
#define NODE 10
#define HEARTBEAT 400000
#define SCAN 500000
#define FAILURE 1300

using namespace std;

class Daemon{
private:
    // for introducers
    string knownHostAsIntroducer;

    // Sockets
    UDPSocket messageSocket;
    UDPSocket commandSocket;
    UDPSocket outSocket;

    // Two Lists
    map<int, VirtualMachine> membershipList;
    map<int, long long int> contactList;

    // Self Properties
    string selfIpAddress;
    string selfLogFileName;
    int selfIndex;
    bool leaveFlag;
    long long int selfTimestamp;

    // mutexs
    mutex membershipListLocker;
    mutex logFileLocker;
public:
    Daemon(bool firstServerFlag);

    void join();
    void heartbeat();
    void checker();
    void command();
    void receive();
    void start();

    // receiver handler functions
    void joinHandler(char * ip);
    void updateHandler(string message);
    void heartbeatHandler(char * ip);

    int newMember(char * ipAddr);
    void updateContact(long long ts);
    void setMemberList(string s);
    string contactsToString();
    string membershipsToString();

    // helper functions
    long int getTimestamp();
    void log(string s, int flag = 0);
    void log(const char * fmt, ...);
    void plog(string s);
    void plog(const char * fmt, ...);
    void setSelfIpAddress();
    void setLogFileName();
    bool dropMessage();
};

#endif // DAEMON_H
