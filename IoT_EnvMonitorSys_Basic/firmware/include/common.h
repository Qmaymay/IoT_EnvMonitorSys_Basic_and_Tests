#ifndef COMMON_H
#define COMMON_H

#include <stdint.h>
#include <stdbool.h>

// 设备配置
#define DEVICE_ID "env_monitor_basic_001"
#define FIRMWARE_VERSION "1.0.0"
#define FEATURE_SET "basic-loop"

// 传感器数据结构
typedef struct {
    float temperature;     // 温度 °C
    float humidity;        // 湿度 %
    float air_quality;     // 空气质量指数
    uint32_t timestamp;    // 时间戳
} sensor_data_t;

// 设备状态
typedef enum {
    DEVICE_NORMAL,
    DEVICE_ERROR,
    DEVICE_CALIBRATING
} device_state_t;

// 通用函数声明
void delay_ms(uint32_t ms);
uint32_t get_timestamp(void);

#endif // COMMON_H