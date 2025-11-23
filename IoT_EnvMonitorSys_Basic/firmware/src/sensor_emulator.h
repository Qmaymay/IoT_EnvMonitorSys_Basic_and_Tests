#ifndef SENSOR_EMULATOR_H
#define SENSOR_EMULATOR_H

#include "common.h"

result_code_t sensor_emulator_init(void);
result_code_t sensor_emulator_read(sensor_data_t* data);

#endif