CC		= g++

SRC_FOLDER=src
INCLUDE_FOLDER=include
CFLAGS=-I$(INCLUDE_FOLDER) -c -Wall -std=c++11 -pthread
LDFLAGS=-pthread
SOURCES=$(wildcard $(SRC_FOLDER)/*.cpp)
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=daemon

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
		$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
		$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(SRC_FOLDER)/*.o
	rm -f $(EXECUTABLE)