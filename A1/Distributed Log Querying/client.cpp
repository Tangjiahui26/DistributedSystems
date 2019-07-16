#include <iostream>
#include <sys/types.h>
#include <stdlib.h>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netinet/tcp.h>
#include <netdb.h>
#include <errno.h>
#include <pthread.h>
#include <sstream>
#include <string.h>
#include <algorithm>
#include <vector>

using namespace std;
#define VMNUMBER 6
#define PORTNUMBER 5330

int connectToServer(char *hostname, int port);
void* receiveData(void* data);

// create a struct to deal with data from each VM
struct vmData {
    int vmId;
    string log;
    int socketNum;
};

// hardcoded servername

string serverNames[6] = {"54.193.91.241",
                         "13.57.234.1",
                         "13.57.238.30",
                         "54.193.37.145",
                         "54.193.77.234",
                         "54.219.130.46"};

int main(int argc, char** argv)
{
    // use stringstream to pass arguments
    stringstream ss;
    for (int i = 0; i < argc; ++i) {
        ss << argv[i] << " ";
    }
    ss << "\n";
    ss.seekg(0, ios::end);

    bool isRun[VMNUMBER];
    int sockets[VMNUMBER];

    // initialize all VMs
    for (int i = 0; i < VMNUMBER; ++i) {
        isRun[i] = false;
    }

    // pass the arguments to each VM after connection
    for (int i = 0; i < VMNUMBER; ++i) {
        sockets[i] = connectToServer((char*) serverNames[i].c_str(), PORTNUMBER);
        if (sockets[i] < 0) {
            cerr << "Failed to Connect to Socket " << i+1 << "Due to " << errno << endl;
            continue;
        }

        int send = write(sockets[i], ss.str().c_str(), ss.str().size());
        if (send < 0) {
            cerr << "Failed to Send to Socket " << i+1 << "Due to " << errno << endl;
            continue;
        } else if (send < ss.tellg()) {
            cerr << "Arguments are Too Long. Please use an originzed pattern." << endl;
        }
        isRun[i] = true;
    }

    //After connected and send pattern to server,
    //We are waiting for the response from server

    // Mutli-threading Initialization
    pthread_t threads[VMNUMBER];
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    string returnResults[VMNUMBER];
    int lineCount[VMNUMBER];
    vmData myData[VMNUMBER];

    // create a thread to receive data for each socket
    for (int i = 0; i < VMNUMBER; ++i) {
        returnResults[i] = "";
        lineCount[i] = 0;
        if (! isRun[i]) {
            continue;
        }
        myData[i].vmId = i;
        myData[i].log = "";
        myData[i].socketNum = sockets[i];
        pthread_create(&threads[i], NULL, receiveData, (void *) (&myData[i]));
    }
    pthread_attr_destroy(&attr);

    // join all the data we received
    void * ret;
    for (int i = 0; i < VMNUMBER; ++i) {
        if (!isRun[i]) {
            continue;
        }
        pthread_join(threads[i], &ret);
        returnResults[i] = *((string *) ret);
    }

    // count the lines received from each VM
    for (int i = 0; i < VMNUMBER; ++i) {
        if(returnResults[i].size() == 0) {
            continue;
        }
        lineCount[i] = std::count(returnResults[i].begin(), returnResults[i].end(), '\n');
        cout << "From " << serverNames[i].c_str() << ": "  << endl;
        cout <<  returnResults[i].c_str() << endl;
     }

    int total = 0;
    for (int i = 0; i < VMNUMBER; ++i) {
        if (returnResults[i].size() == 0) {
            if (isRun[i]) {
                cout << "No Results from machine." << i+1 << ".log in" << serverNames[i].c_str() << endl;
            } else {
                cout << "No Results from machine." << i+1 << ".log in"
                     << serverNames[i].c_str() << ": Server cannot be connected." << endl;
            }
            continue;
        }
        total += lineCount[i];
        cout << lineCount[i] << " lines matched from machine." << i+1 << ".log in"
             << serverNames[i].c_str() << endl;
    }
    cout << "Total lines matched: " << total << endl;

    // close the sockets
    for (int i = 0; i < VMNUMBER; ++i) {
        close(sockets[i]);
    }
}

// connect function for each hardcoded server
int connectToServer(char* hostname, int port){
    // create a TCP socket
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd == -1) {
        cout << "Failed to create a socket" << endl;
        return -1;
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = inet_addr(hostname);

    // Try to bind connection
    int res = connect(socket_fd, (struct sockaddr*)&addr, sizeof(addr));
    if (res == -1) {
        cout <<"Failed to bind connection" << endl;
        return -1;
    }
    cout << "Binded Connection" << endl;
    return socket_fd;
}

// After connecting to the server, we need to receive
// Data for each VM using multithreading
void* receiveData(void *data) {
    char buf[4096];
    int received = 0;
    vmData * myData = (vmData*) data;
    int vmId = myData->vmId;

    // Keep receiving data from socket
    do {
       received = recv(myData->socketNum, buf, 4096, 0);
       if (received == -1) {
           myData->log = "";
           cout << "Cannot Receive Data from Socket " << vmId+1 << " Due to " << errno;
           pthread_exit((void*)&myData->log);
       } else {
           myData->log += string(buf, received);
       }
    } while (received > 0);
    pthread_exit((void*)&myData->log);
}
