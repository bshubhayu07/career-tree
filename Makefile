# Makefile for CareerTree Pure C Implementation
CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99
TARGET = career_tree.exe

SRCS = main.c tree.c
OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

%.o: %.c tree.h
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	del /Q $(OBJS) $(TARGET) career_recommendation.txt 2>nul || rm -f $(OBJS) $(TARGET) career_recommendation.txt

.PHONY: all run clean
