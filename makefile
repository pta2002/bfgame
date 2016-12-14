CC=g++
CFLAGS=-Wall
TARGET=bin/bfgame

INCLUDES:=-I./include
LIBS=
SRCS:=$(wildcard src/*.cpp)
OBJS:=$(patsubst %.cpp,%.o,$(SRCS))

all: build

.PHONY: clean

build: $(OBJS)
	$(CC) $(CFLAGS) $(INCLUDES) -o $(TARGET) $(OBJS) $(LIBS)

.cpp.o: includes/*
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	$(RM) *.o *~ $(TARGET)
