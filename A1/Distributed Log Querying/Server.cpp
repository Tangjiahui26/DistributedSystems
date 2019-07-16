#include <iostream>
#include <sys/types.h>
#include <stdlib.h>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <sys/wait.h>
#include <netdb.h>
#include <map>
#include <string.h>

using namespace std;
#define VMNUMBER 6
#define PORTNUMBER 5330
#define HOSTNAMELENGTH 64

static map<string, string> serverNames = {{"ip-172-31-28-99", "/home/ubuntu/machine.1.log"},
                                   {"ip-172-31-26-191", "/home/ubuntu/machine.2.log"},
                                   {"ip-172-31-25-60", "/home/ubuntu/machine.3.log"},
                                   {"ip-172-31-28-127", "/home/ubuntu/machine.4.log"},
                                   {"ip-172-31-23-68", "/home/ubuntu/machine.5.log"},
                                   {"ip-172-31-16-232", "/home/ubuntu/machine.6.log"}};

void handleRequest(int fd);
string getLogFileName();

void processHandler(int signum) {
    while(waitpid(-1, NULL, WNOHANG) != -1);
}

int main(int argc, char * argv[])
{
    // clean all the child processes before accept connection
    signal(SIGCHLD, processHandler);

    // create server socket
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd == -1) {
        cout << "Failed to Create Server Socket" << endl;
        exit(-1);
    }

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORTNUMBER);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    int reuseAddr = 1;
    int setOption = setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &reuseAddr, sizeof(reuseAddr));
    if (setOption == -1) {
        cout << "Failed to set sockopt" << endl;
        exit(-1);
    }

    // bind()
    int res = bind(socket_fd, (struct sockaddr*)&addr, sizeof(addr));
    if (res == -1) {
        cout << "Failed to bind socket" << endl;
        exit(-1);
    }

    // keep listening
    int listenRes = listen(socket_fd, 1);
    if (listenRes != 0) {
        cout << "Failed to listen socket" << endl;
        exit(-1);
    }

    // accept connection
    struct sockaddr_in cli_addr;
    int clilen = sizeof(cli_addr);
    while(1) {
        int fd = accept(socket_fd, (struct sockaddr *)&cli_addr, (socklen_t *)&clilen);
        if (fd == -1){
            if(errno == EINTR) {
                continue;
            } else {
                perror("Accept Error");
            }
        } else {
            handleRequest(fd);
            cout << "Handling Request" << endl;
        }
    }
    return 0;
}

string getLogFileName(){
    char hostname[HOSTNAMELENGTH];
    hostname[HOSTNAMELENGTH -1 ] = '\0';
    gethostname(hostname, HOSTNAMELENGTH);
    std::string hostnameString(hostname);
    return serverNames.at(hostnameString);
}

void handleRequest(int fd) {
    char *args[16];
    char request[1024];
    FILE *fpin = fdopen(fd, "r");
    fgets(request, 1024, fpin);
    string grep = "/bin/grep";
    // use -H and -n options here to print file name and line number
    string options = "-Hn";
    args[0] = (char *)grep.c_str();
    args[1] = (char *)options.c_str();

    // parse the arguments from client
    const char delim[] = "\t\r\n\"";
    char * buf = strtok(request, delim);
    buf = strtok(NULL, delim);
    args[2] = buf;
    string fileName = getLogFileName();
    args[3] = (char *) fileName.c_str();
    args[4] = NULL;

    int pid = fork();
    if (pid == -1) {
        perror("Fork Error");
        return;
    }
    if (pid == 0) {
        // redirect standard output
        dup2(fd, 1);
        // redirect standard error
        dup2(fd, 2);
        close(fd);
        execvp(args[0], args);
        perror("Grep Error");
    } else {
        close(fd);
    }
}
