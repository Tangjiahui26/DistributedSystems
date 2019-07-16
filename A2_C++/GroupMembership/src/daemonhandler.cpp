#include "daemon.h"

void Daemon::joinHandler(char *ip){
    int remotePos = 0;
    remotePos = newMember(ip);

    plog("join update memebrship list %s", membershipsToString().c_str());
    plog("join update contact list %s", contactsToString().c_str());

    string ret = "reply";
    ret += "," + to_string(remotePos);
    ret += "," + to_string(membershipList.size());

    for (auto it = membershipList.begin(); it != membershipList.end(); it++) {
        ret += "," + (it->second).toString();
    }

    messageSocket.send(ip, ret.c_str());

    for (auto it = contactList.begin(); it != contactList.end(); it++) {
        string info = "update,join," + membershipList[remotePos].toString();
        messageSocket.send(membershipList[it->first].ipAddress.c_str(), info.c_str());
    }
}

void Daemon::updateHandler(string message) {
    string backupMessage = message;

    // join
    if(message[7] == 'j') {
        message = message.substr(12, message.length());
        VirtualMachine tmp(message);
        if(membershipList.find(tmp.id) != membershipList.end()) {
            return;
        } else {
            plog(backupMessage);
            membershipList[tmp.id] = tmp;
            long int ts = getTimestamp();
            updateContact(ts);

            for (auto it = contactList.begin(); it != contactList.end(); it++) {
                messageSocket.send(membershipList[it->first].ipAddress.c_str(), backupMessage.c_str());
            }
            plog("Join update membership list: %s", membershipsToString().c_str());
            plog("Join update contact list: %s", contactsToString().c_str());
        }
    } else if (message[7] == 'c') {
        message = message.substr(13, message.length());
        VirtualMachine tmp(message);
        if(membershipList.find(tmp.id) != membershipList.end()) {
            return;
        } else {
            plog(backupMessage);
            membershipList.erase(tmp.id);
            long int ts = getTimestamp();
            updateContact(ts);

            for (auto it = contactList.begin(); it != contactList.end(); it++) {
                messageSocket.send(membershipList[it->first].ipAddress.c_str(), backupMessage.c_str());
            }
            plog("Crash update membership list: %s", membershipsToString().c_str());
            plog("Crash update contact list: %s", contactsToString().c_str());
        }
    } else {
        message = message.substr(13, message.length());
        VirtualMachine tmp(message);
        if(membershipList.find(tmp.id) != membershipList.end()) {
            return;
        } else {
            plog(backupMessage);
            membershipList.erase(tmp.id);
            long int ts = getTimestamp();
            updateContact(ts);

            for (auto it = contactList.begin(); it != contactList.end(); it++) {
                messageSocket.send(membershipList[it->first].ipAddress.c_str(), backupMessage.c_str());
            }
            plog("Leave update membership list: %s", membershipsToString().c_str());
            plog("Leave update contact list: %s", contactsToString().c_str());
        }
    }
}

 void Daemon::heartbeatHandler(char *ip) {
    long long ts = getTimestamp();
    string rip = ip;

    for (auto it = contactList.begin(); it != contactList.end(); it++) {
        if (membershipList[it->first].ipAddress == rip){
            contactList[it->first] = ts;
            log("Heartbeat from %s", ip);
        }
    }
}
