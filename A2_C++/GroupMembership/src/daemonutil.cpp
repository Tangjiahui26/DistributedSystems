#include "daemon.h"

long int Daemon::getTimestamp(){
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long int currentTime = tv.tv_sec * 1000 + tv.tv_usec /1000;
    return currentTime;
}

void Daemon::log(string s, int flag){
    logFileLocker.lock();
    long int ts = getTimestamp();
    double fts = (double) ts /1000.0;
    FILE *fp = fopen(selfLogFileName.c_str(), "a");
    fprintf(fp, "[%02d-%.3f] %s\n", selfIndex, fts, s.c_str());
    fclose(fp);

    // explicit print
    if (flag == 1) {
        printf("[%02d-%.3f] %s\n", selfIndex, fts, s.c_str());
    }

    logFileLocker.unlock();
}

void Daemon::log(const char *fmt, ...){
    char buf[1024];
    va_list args;
    va_start(args, fmt);
    vsprintf(buf, fmt, args);
    va_end(args);
    log(string(buf), 0);
}

void Daemon::plog(string s){
    log(s, 1);
}

void Daemon::plog(const char *fmt, ...){
    char buf[1024];
    va_list args;
    va_start(args, fmt);
    vsprintf(buf, fmt, args);
    va_end(args);
    log(string(buf), 1);
}

void Daemon::setSelfIpAddress(){
    map<string, string> privateToPublic =
                      {{"172.31.28.99", "54.193.91.241"},
                       {"172.31.26.191", "13.57.234.1"},
                       {"172.31.25.60", "13.57.238.30"},
                       {"172.31.28.127", "54.193.37.145"},
                       {"172.31.23.68", "54.193.77.234"},
                       {"172.31.16.232", "54.219.130.46"}};

    struct ifaddrs * ifAddrsStruct = NULL;
    struct ifaddrs * ifa = NULL;
    void * temp;

    getifaddrs(&ifAddrsStruct);

    for (ifa = ifAddrsStruct; ifa != NULL; ifa = ifa->ifa_next) {
        if (!ifa->ifa_addr){
            continue;
        }

        // using IPv4
        if (ifa->ifa_addr->sa_family == AF_INET) {
            temp = &((struct sockaddr_in *) ifa->ifa_addr)->sin_addr;
            char addressBuffer[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, temp, addressBuffer, INET_ADDRSTRLEN);
            if (strcmp(ifa->ifa_name, "eth0") == 0){
                selfIpAddress = addressBuffer;
                selfIpAddress = privateToPublic.at(selfIpAddress);
            }
        }
    }
    if(ifAddrsStruct!=NULL) {
        freeifaddrs(ifAddrsStruct);
    }
}

void Daemon::setLogFileName(){
    selfLogFileName = "server" + selfIpAddress + ".log";
}

bool Daemon::dropMessage(){
    int ans = rand() % 100;
    if (ans < DROPRATE) return true;
    return false;
}
