#include "daemon.h"

using namespace std;

int main(int argc, char* argv[])
{
    int flag = 0;
    if (argc > 1) {
        flag = 1;
    }

    Daemon myServer(flag);

    std::thread recv_t (&Daemon::receive, &myServer);
    std::thread heartbeat_t (&Daemon::heartbeat, &myServer);
    std::thread checker_t (&Daemon::checker, &myServer);
    std::thread command_t (&Daemon::command, &myServer);

    recv_t.join();
    heartbeat_t.join();
    checker_t.join();
    command_t.join();
}
