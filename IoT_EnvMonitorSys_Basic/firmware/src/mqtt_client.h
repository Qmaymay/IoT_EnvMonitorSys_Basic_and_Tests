#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include "common.h"

bool mqtt_connect(void);
void mqtt_disconnect(void);
bool mqtt_publish_sensor_data(const sensor_data_t* data);

#endif