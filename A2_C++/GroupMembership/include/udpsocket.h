#ifndef UDPSOCKET_H
#define UDPSOCKET_H

#include <string>
#include <cstdlib>
#include <cstring>
#include <netdb.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <string.h>
#include <iostream>

#define BUFSIZE 4096

using namespace std;

class UDPSocket
{
private:
    struct sockaddr_in serverAddress, clientAddress, sendAddress, receiveAddress;
    int serverSocketFd, clientSocketFd;
    int portNumber;
public:
    UDPSocket(int port);
    UDPSocket(int port, bool send);
    void setTimeout(int time);
    int send(const char* ip, const char* message);
    int receive(char*ip, char* message);
};

#endif // UDPSOCKET_H
