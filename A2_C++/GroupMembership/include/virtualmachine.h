#ifndef VIRTUALMACHINE_H
#define VIRTUALMACHINE_H

#include <string>

using namespace std;

class VirtualMachine{
public:
    string ipAddress;
    long long int timestamp;
    int id;
    VirtualMachine() {}
    VirtualMachine(string s);
    VirtualMachine(const VirtualMachine &tmp);
    VirtualMachine(string _ipAddress, long long int _time);
    VirtualMachine(string _ipAddress, long long _time, int _id);

    string toString();
};

#endif // VIRTUALMACHINE_H
