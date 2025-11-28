#define ENV_MONITOR_DLL_EXPORTS
#include <stdio.h> 
#include "sensor_emulator.h"
#include "common.h"
#include "config.h"
#include <stdlib.h>
#include <time.h>


uint32_t get_timestamp(void) {
    return (uint32_t)time(NULL);
}


result_code_t sensor_emulator_init(void) {
    printf("[SENSOR] Sensor emulator initialized\n");
    srand((unsigned int)time(NULL));  // 随机数种子
    return RESULT_OK;
}


result_code_t sensor_emulator_read(sensor_data_t* data) {
    if (data == NULL) {
        return RESULT_INVALID_PARAM;
    }
    
    static uint16_t sequence_counter = 0;
    
    // 中国各地区秋冬季特征
    typedef enum {
        GUANGDONG_GUANGXI,   // 广东广西：温暖潮湿
        ZHEJIANG_ANHUI,      // 浙江安徽：温和湿润
        BEIJING_TIANJIN,     // 北京天津：干燥凉爽
        DONGBEI,             // 东北三省：寒冷干燥
        NORTHWEST,           // 西北地区：干燥大风
        XINJIANG,            // 新疆：昼夜温差大
        XIZANG,              // 西藏：寒冷紫外线强
        CHUANYU              // 川渝：潮湿多雾
    } region_type_t;
    
    // 随机选择一个地区
    region_type_t region = rand() % 8;
    
    switch(region) {
        case GUANGDONG_GUANGXI:  // 广东广西：温暖潮湿
            data->temperature = 18.0f + (float)(rand() % 120) / 10.0f;  // 18.0-30.0°C
            data->humidity = 70.0f + (float)(rand() % 300) / 10.0f;     // 70.0-100.0%
            data->air_quality = 65.0f + (float)(rand() % 350) / 10.0f;  // 65.0-100.0%
            printf("[SENSOR] 🌊 两广地区: ");
            break;
            
        case ZHEJIANG_ANHUI:     // 浙江安徽：温和湿润
            data->temperature = 12.0f + (float)(rand() % 130) / 10.0f;  // 12.0-25.0°C
            data->humidity = 65.0f + (float)(rand() % 350) / 10.0f;     // 65.0-100.0%
            data->air_quality = 70.0f + (float)(rand() % 300) / 10.0f;  // 70.0-100.0%
            printf("[SENSOR] 🍃 江浙地区: ");
            break;
            
        case BEIJING_TIANJIN:    // 北京天津：干燥凉爽
            data->temperature = 5.0f + (float)(rand() % 150) / 10.0f;   // 5.0-20.0°C
            data->humidity = 30.0f + (float)(rand() % 400) / 10.0f;     // 30.0-70.0%
            data->air_quality = 60.0f + (float)(rand() % 400) / 10.0f;  // 60.0-100.0%
            printf("[SENSOR] 🏙️ 京津地区: ");
            break;
            
        case DONGBEI:            // 东北三省：寒冷干燥
            data->temperature = -15.0f + (float)(rand() % 250) / 10.0f; // -15.0-10.0°C
            data->humidity = 25.0f + (float)(rand() % 350) / 10.0f;     // 25.0-60.0%
            data->air_quality = 80.0f + (float)(rand() % 200) / 10.0f;  // 80.0-100.0%
            printf("[SENSOR] 🌲 东北地区: ");
            break;
            
        case NORTHWEST:          // 西北地区：干燥大风
            data->temperature = 0.0f + (float)(rand() % 200) / 10.0f;   // 0.0-20.0°C
            data->humidity = 20.0f + (float)(rand() % 300) / 10.0f;     // 20.0-50.0%
            data->air_quality = 75.0f + (float)(rand() % 250) / 10.0f;  // 75.0-100.0%
            printf("[SENSOR] 🏜️ 西北地区: ");
            break;
            
        case XINJIANG:           // 新疆：昼夜温差大
            data->temperature = -5.0f + (float)(rand() % 300) / 10.0f;  // -5.0-25.0°C
            data->humidity = 15.0f + (float)(rand() % 350) / 10.0f;     // 15.0-50.0%
            data->air_quality = 85.0f + (float)(rand() % 150) / 10.0f;  // 85.0-100.0%
            printf("[SENSOR] 🐫 新疆地区: ");
            break;
            
        case XIZANG:             // 西藏：寒冷紫外线强
            data->temperature = -10.0f + (float)(rand() % 250) / 10.0f; // -10.0-15.0°C
            data->humidity = 25.0f + (float)(rand() % 300) / 10.0f;     // 25.0-55.0%
            data->air_quality = 90.0f + (float)(rand() % 100) / 10.0f;  // 90.0-100.0%
            printf("[SENSOR] 🏔️ 西藏地区: ");
            break;
            
        case CHUANYU:            // 川渝：潮湿多雾
            data->temperature = 8.0f + (float)(rand() % 120) / 10.0f;   // 8.0-20.0°C
            data->humidity = 75.0f + (float)(rand() % 250) / 10.0f;     // 75.0-100.0%
            data->air_quality = 55.0f + (float)(rand() % 450) / 10.0f;  // 55.0-100.0%
            printf("[SENSOR] 🌫️ 川渝地区: ");
            break;
    }
    
    data->timestamp = get_timestamp();
    data->sequence = sequence_counter++;
    
    printf("温度%.1f°C, 湿度%.1f%%, 空气质量%.1f%%, 序列号%d\n", 
           data->temperature, data->humidity, data->air_quality, data->sequence);
    
    return RESULT_OK;
}

float sensor_get_temperature(void) {
    sensor_data_t data;
    if (sensor_emulator_read(&data) == RESULT_OK) {
        return data.temperature;
    }
    return 25.0f;
}

float sensor_get_humidity(void) {
    sensor_data_t data;
    if (sensor_emulator_read(&data) == RESULT_OK) {
        return data.humidity;
    }
    return 60.0f;
}

float sensor_get_air_quality(void) {
    sensor_data_t data;
    if (sensor_emulator_read(&data) == RESULT_OK) {
        return data.air_quality;
    }
    return 85.0f;
}


