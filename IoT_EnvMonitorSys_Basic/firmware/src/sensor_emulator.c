// #include "common.h"
// #include "config.h"
// #include <stdlib.h>

// // 模拟传感器数据生成
// sensor_data_t read_sensor_data(void) {
//     sensor_data_t data;
    
//     // 模拟温度读数 (15-35°C 范围内)
//     data.temperature = 15.0 + (rand() % 200) * 0.1;
    
//     // 模拟湿度读数 (30-80%)
//     data.humidity = 30.0 + (rand() % 500) * 0.1;
    
//     // 模拟空气质量 (0-100)
//     data.air_quality = (rand() % 1000) * 0.1;
    
//     // 时间戳
//     data.timestamp = get_timestamp();
    
//     return data;
// }

// // 数据验证
// bool validate_sensor_data(const sensor_data_t* data) {
//     if (data->temperature < TEMPERATURE_RANGE_MIN || 
//         data->temperature > TEMPERATURE_RANGE_MAX) {
//         return false;
//     }
//     if (data->humidity < 0 || data->humidity > 100) {
//         return false;
//     }
//     return true;
// }  
#include <stdio.h> 
#include "sensor_emulator.h"
#include "common.h"
#include "config.h"
#include <stdlib.h>
#include <time.h>

// 添加函数声明
uint32_t get_timestamp(void);

result_code_t sensor_emulator_init(void) {
    printf("[SENSOR] Sensor emulator initialized\n");
    srand((unsigned int)time(NULL));  // 随机数种子
    return RESULT_OK;
}

result_code_t sensor_emulator_read(sensor_data_t* data) {
    if (data == NULL) {
        return RESULT_INVALID_PARAM;
    }
    
    // 生成模拟传感器数据
    data->temperature = 15.0f + (float)(rand() % 300) / 10.0f;  // 15.0 - 45.0
    data->humidity = 30.0f + (float)(rand() % 700) / 10.0f;     // 30.0 - 100.0
    data->air_quality = (float)(rand() % 1000) / 10.0f;         // 0.0 - 100.0
    data->timestamp = get_timestamp();
    
    return RESULT_OK;
}

// 在 sensor_emulator.c 中也添加这个函数
uint32_t get_timestamp(void) {
    return (uint32_t)time(NULL);
}