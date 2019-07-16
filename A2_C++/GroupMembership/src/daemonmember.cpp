#include "daemon.h"

void Daemon::updateContact(long long ts){
    vector<int> index;
    int tmp = 0;
    int my_loc = 0;
    int left_cnt = 0;
    int right_cnt = 0;

    contactList.clear();

    for (auto it = membershipList.begin(); it != membershipList.end(); it++) {
        index.push_back(it->first);
    }

    sort(index.begin(), index.end());
    for (auto i = 0; i < int(index.size()); i++) {
        if (index[i] == selfIndex){
            my_loc = i;
            break;
        }
    }

    tmp = my_loc + 1;
    while (right_cnt < 2 && tmp != my_loc) {
        if (tmp == int(index.size())) {
            tmp = 0;
        }
        if (tmp == my_loc) {
            break;
        }
        contactList[index[tmp]] = ts;
        right_cnt++;
        tmp++;
    }

    tmp = my_loc - 1;
    while (left_cnt < 2 && tmp != my_loc) {
        if (tmp == -1) {
            tmp = int(index.size()) - 1;
        }

        if (tmp == my_loc) {
            break;
        }
        contactList[index[tmp]] = ts;
        left_cnt++;
        tmp--;
    }
    plog("Update contact list: %s", contactsToString().c_str());
}

int Daemon::newMember(char *ipAddr) {
    long int ts = getTimestamp();
    int remotePos = 0;
    for (int i = 1; i <= NODE; i++) {
        if (membershipList.find(i) == membershipList.end()){
            string rip = ipAddr;
            VirtualMachine tmp(rip, ts, i);
            membershipList[i] = tmp;
            remotePos = i;
            plog("Insert %s in %dth position", ipAddr, remotePos);
            break;
        }
    }
    updateContact(ts);
    return remotePos;
}

void Daemon::setMemberList(string s){
    int pIndex = s.find(",");
    s = s.substr(pIndex+1, s.length());
    while (s.length()) {
        pIndex = s.find(",");
        if(pIndex == -1) {
            pIndex = s.length();
        }

        VirtualMachine newNode(s.substr(0, pIndex));
        membershipList[newNode.id] = newNode;
        if (pIndex < int(s.length())) {
            s = s.substr(pIndex+1, s.length());
        } else {
            break;
        }
    }
}

string Daemon::membershipsToString() {
    string ret  = "";
    ret += to_string(membershipList.size());
    for (auto it = membershipList.begin(); it != membershipList.end(); it++) {
        ret += ", " + (it->second).toString();
    }
    return ret;
}

string Daemon::contactsToString(){
    string ret = "";
    ret += to_string(contactList.size());
    for (auto it = contactList.begin(); it != contactList.end(); it++) {
        ret += ", " + to_string(it->first)  + "/" + to_string(it->second);
    }
    return ret;
}
