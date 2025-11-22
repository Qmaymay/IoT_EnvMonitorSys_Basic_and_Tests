#ifndef SENSOR_EMULATOR_H
#define SENSOR_EMULATOR_H

#include "common.h"

sensor_data_t read_sensor_data(void);
bool validate_sensor_data(const sensor_data_t* data);

#endif
