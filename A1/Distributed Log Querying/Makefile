CPPC            = g++

all: client Server

client: client.o 
	$(CPPC) -o client client.o -lpthread

Server: Server.o 
	$(CPPC) -o Server Server.o

client.o: client.cpp
	$(CPPC) -c client.cpp

Server.o: Server.cpp
	$(CPPC) -c Server.cpp


clean:
	rm -r Server client Server.o client.o