#include "daemon.h"

Daemon::Daemon(bool firstServerFlag): messageSocket(UDPSocket(53310)),
                                      commandSocket(UDPSocket(53311)),
                                      outSocket(UDPSocket(53312)){
    // clear all the lists
    membershipList.clear();
    contactList.clear();

    srand(time(NULL));

    setSelfIpAddress();
    setLogFileName();
    leaveFlag = false;

    string introducer = "54.193.91.241";
    knownHostAsIntroducer = introducer;
    plog("%s is a known introducer", introducer.c_str());

    // only for the first server
    if ((firstServerFlag) &&
        (strcmp(selfIpAddress.c_str(), knownHostAsIntroducer.c_str()) == 0)) {
        plog("First Node starts.");
        selfIndex = 1;
        long long int currentTime = getTimestamp();
        VirtualMachine tmp(selfIpAddress, currentTime, selfIndex);
        membershipList[selfIndex] = tmp;
    } else{
           join();
       }
}

void Daemon::join() {
    int index;

    // if it is the introducer, then do nothing
    if (strcmp(selfIpAddress.c_str(), knownHostAsIntroducer.c_str()) == 0)
        return;

    // send message "join"
    messageSocket.send(knownHostAsIntroducer.c_str(), "join");
    plog("SEND END");
    char buf[BUFSIZE], rip[100];
    int res = 0;
    messageSocket.setTimeout(500000);
    res = messageSocket.receive(rip, buf);

    if (res <= 0) {
        plog("Introducer time out for join");
        return;
    }

    messageSocket.setTimeout(0);
    string w = buf;
    // NOT "reply" message
    if (w[0] != 'r'){
        return;
    }

    // parse message
    index = w.find(",");
    w = w.substr(index + 1, w.length());
    index = w.find(",");
    selfIpAddress = stoi(w.substr(0, index));
    setMemberList(w);
    long int ts = getTimestamp();
    updateContact(ts);
}

void Daemon::command(){
    plog("Monintoring commands from users");
    while(leaveFlag == false) {
        char buf[BUFSIZE];
        char rip[BUFSIZE];
        commandSocket.receive(rip, buf);
        plog("[cmd debug] %s", buf);

        string msg;
        switch (buf[0]) {
        case 'l':
            plog("[cmd debug] leave should happen");
            for (auto it = contactList.begin(); it != contactList.end(); it++) {
                string info = "update,leave," + membershipList[selfIndex].toString();
                messageSocket.send(membershipList[it->first].ipAddress.c_str(), info.c_str());
            }
            leaveFlag = true;
            break;
        case 'i':
            msg = membershipList[selfIndex].toString();
            outSocket.send(rip, msg.c_str());
            break;
        case 'm':
            msg = membershipsToString();
            outSocket.send(rip, msg.c_str());
            break;
        default:
            break;
        }
    }
}

void Daemon::heartbeat(){
    while(leaveFlag == false) {
       usleep(HEARTBEAT);
       for (auto it = contactList.begin(); it != contactList.end(); it++) {
           string info = "heartbeat";
           if (!dropMessage()) {
               messageSocket.send(membershipList[it->first].ipAddress.c_str(), info.c_str());
           }
       }
    }
    plog("HEARTBEAT EXIT");
}

void Daemon::checker(){
    while(leaveFlag == false) {
        usleep(SCAN);

        long int ts = getTimestamp();
        vector<int> toBeRemovedNodes;
        vector<string> deleteNodes;

        for (auto it = contactList.begin(); it != contactList.end(); it++) {
            if((ts - it->second) > FAILURE) {
                plog("crash %d(%s/%11d) failed (latest %11d)", it->first, membershipList[it->first].ipAddress.c_str(),
                                                               membershipList[it->first].timestamp, it->second);
                toBeRemovedNodes.push_back(it->first);
            }
        }

        for (auto it = toBeRemovedNodes.begin(); it != toBeRemovedNodes.end(); it++) {
            int pos = *it;
            deleteNodes.push_back(membershipList[pos].toString());
            membershipList.erase(pos);
            updateContact(ts);
        }

        for (auto it = deleteNodes.begin(); it != deleteNodes.end(); it++) {
            string info = "update,crash," + (*it);
            for (auto it = contactList.begin(); it != contactList.end(); it++) {
                messageSocket.send(membershipList[it->first].ipAddress.c_str(), info.c_str());
            }
        }

        if(toBeRemovedNodes.size() > 0) {
            plog("crash update member list %s", membershipsToString().c_str());
            plog("crash update contact list %s", contactsToString().c_str());
        }
    }
    plog("CHECKER EXIT");
}

void Daemon::receive() {
    while(leaveFlag == false) {
        char buf[BUFSIZE];
        char rip[BUFSIZE];
        messageSocket.receive(rip, buf);
        string s(rip);
        plog("AAAA %s", s.c_str());
        switch (buf[0]) {
        case 'j':
            joinHandler(rip);
            break;
        case 'h':
            heartbeatHandler(rip);
            break;
        case 'u':
            updateHandler(string(buf));
            break;
        default:
            break;
        }
    }
    plog("RECEIVE EXIT");
}
