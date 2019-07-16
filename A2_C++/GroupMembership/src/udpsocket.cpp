#include "udpsocket.h"

UDPSocket::UDPSocket(int port){
    portNumber = port;

    // create server socket using UDP
    serverSocketFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (serverSocketFd == -1) {
        perror("Failed to create a server socket");
    }

    memset((char *) &serverAddress, 0, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(portNumber);
    serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);

    // Try to bind
    int res1 = bind(serverSocketFd, (struct sockaddr*)&serverAddress, sizeof(serverAddress));
    if (res1 == -1) {
        perror("Failed to bind server socket");
    }

    // create client socket using UDP
    clientSocketFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (clientSocketFd == -1) {
        perror("Failed to create a client socket");
    }

    memset((char *) &clientAddress, 0, sizeof(clientAddress));
    clientAddress.sin_family = AF_INET;
    // bind to any port number
    clientAddress.sin_port = htons(0);
    clientAddress.sin_addr.s_addr = htonl(INADDR_ANY);

    // Try to bind
    int res2 = bind(clientSocketFd, (struct sockaddr*)&clientAddress, sizeof(clientAddress));
    if (res2 == -1) {
        perror("Failed to bind client socket");
    }

    cout << portNumber << "binding finished." << endl;
}

UDPSocket::UDPSocket(int port, bool send){
    portNumber = port;
    if(send) {
        clientSocketFd = socket(AF_INET, SOCK_DGRAM, 0);
        if (clientSocketFd == -1) {
            perror("Failed to create a client socket");
        }

        memset((char *) &clientAddress, 0, sizeof(clientAddress));
        clientAddress.sin_family = AF_INET;
        // bind to any port number
        clientAddress.sin_port = htons(0);
        clientAddress.sin_addr.s_addr = htonl(INADDR_ANY);

        // Try to bind
        int res = bind(clientSocketFd, (struct sockaddr*)&clientAddress, sizeof(clientAddress));
        if (res == -1) {
            perror("Failed to bind client socket");
        }

        cout << portNumber << "binding finished." << endl;
    }
}

void UDPSocket::setTimeout(int time){
    struct timeval _timeval;
    _timeval.tv_sec = 0;
    _timeval.tv_usec = time;
    int res = setsockopt(serverSocketFd, SOL_SOCKET, SO_RCVTIMEO, &_timeval, sizeof(_timeval));
    if(res < 0) {
        perror("Timeout ERROR");
    }
}

int UDPSocket::send(const char *ip, const char *message){
    memset((char *)&sendAddress, 0, sizeof(sendAddress));
    sendAddress.sin_family = AF_INET;
    sendAddress.sin_port = htons(portNumber);
    inet_pton(AF_INET, ip, &(sendAddress.sin_addr));
    int res = sendto(clientSocketFd, message, strlen(message), 0,
                         (struct sockaddr*)&sendAddress, sizeof(sendAddress));
    if (res < 0) {
        perror("Sendto ERROR");
        return -1;
    }
    // ?
    cout << "sendto " << ip << " " << portNumber << " " << message;
    return 0;
}

int UDPSocket::receive(char *ip, char *message){
    socklen_t receiveAddressLength = sizeof(receiveAddress);
    int res;
    res = recvfrom(serverSocketFd, message, BUFSIZE, 0, (struct sockaddr*) &receiveAddress, &receiveAddressLength);
    inet_ntop(AF_INET, &(receiveAddress.sin_addr), ip, INET_ADDRSTRLEN);
    message[res] = '\0';
    // cout << "receive " << ip <<  " " << message;
    return res;
}
