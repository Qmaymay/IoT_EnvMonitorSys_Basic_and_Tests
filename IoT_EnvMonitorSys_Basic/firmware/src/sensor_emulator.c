#include "common.h"
#include "config.h"
#include <stdlib.h>

// 模拟传感器数据生成
sensor_data_t read_sensor_data(void) {
    sensor_data_t data;
    
    // 模拟温度读数 (15-35°C 范围内)
    data.temperature = 15.0 + (rand() % 200) * 0.1;
    
    // 模拟湿度读数 (30-80%)
    data.humidity = 30.0 + (rand() % 500) * 0.1;
    
    // 模拟空气质量 (0-100)
    data.air_quality = (rand() % 1000) * 0.1;
    
    // 时间戳
    data.timestamp = get_timestamp();
    
    return data;
}

// 数据验证
bool validate_sensor_data(const sensor_data_t* data) {
    if (data->temperature < TEMPERATURE_RANGE_MIN || 
        data->temperature > TEMPERATURE_RANGE_MAX) {
        return false;
    }
    if (data->humidity < 0 || data->humidity > 100) {
        return false;
    }
    return true;
}  