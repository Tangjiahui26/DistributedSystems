#include <string>
#include "virtualmachine.h"

using namespace std;

VirtualMachine::VirtualMachine(string _ipAddress, long long _time, int _id){
    ipAddress = _ipAddress;
    timestamp = _time;
    id = _id;
}

// for introducer
VirtualMachine::VirtualMachine(string _ipAddress, long long _time){
    ipAddress = _ipAddress;
    timestamp = _time;
}

VirtualMachine::VirtualMachine(const VirtualMachine &tmp){
    ipAddress = tmp.ipAddress;
    id = tmp.id;
    timestamp = tmp.timestamp;
}

VirtualMachine::VirtualMachine(string s){
    //parsing the string
    int index;
    index = s.find("/");
    id = stoi(s.substr(0, index));
    s = s.substr(index+1, s.length());
    index = s.find("/");
    ipAddress = s.substr(0, index);
    s = s.substr(index+1, s.length());
    timestamp = stoll(s);
}

string VirtualMachine::toString(){
    return to_string(id) + "/" + ipAddress + "/" + to_string(timestamp);
}
