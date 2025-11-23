# Makefile for IoT Environment Monitor

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g
INCLUDES = -I.
SOURCES = main.c sensor_emulator.c mqtt_client.c
OBJECTS = $(SOURCES:.c=.o)
TARGET = iot_env_monitor

# 如果使用Paho MQTT库，取消注释下面的行
# MQTT_LIBS = -lpaho-mqtt3c
LIBS = $(MQTT_LIBS)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJECTS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

debug: $(TARGET)
	gdb ./$(TARGET)
	