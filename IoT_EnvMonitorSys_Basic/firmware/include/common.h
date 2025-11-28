#ifndef COMMON_H
#define COMMON_H

#include <stdint.h>
#include <stdbool.h>
#include "env_monitor_export.h"


// 传感器数据结构
typedef struct {
    float temperature;      // 温度 (°C)
    float humidity;         // 湿度 (%)
    float air_quality;      // 空气质量指数
    uint32_t timestamp;     // 时间戳
    uint16_t sequence;      // 序列号，用于检测数据丢失
} sensor_data_t;

\
// 设备状态结构
typedef struct {
    char device_id[32];
    char firmware_version[16];
    uint32_t uptime_ms;
    uint32_t data_count;
    uint8_t wifi_strength;  // WiFi信号强度 (0-100)
    bool mqtt_connected;
} device_status_t;


// MQTT客户端状态
typedef enum {
    MQTT_STATE_DISCONNECTED,
    MQTT_STATE_CONNECTING,
    MQTT_STATE_CONNECTED,
    MQTT_STATE_ERROR
} mqtt_state_t;

// 函数返回码
typedef enum {
    RESULT_OK = 0,
    RESULT_ERROR = -1,
    RESULT_INVALID_PARAM = -2,
    RESULT_NETWORK_ERROR = -3,
    RESULT_MQTT_ERROR = -4
} result_code_t;

// 函数声明
ENV_MONITOR_API uint32_t get_current_time_ms(void);
ENV_MONITOR_API void network_delay_ms(uint32_t ms);
ENV_MONITOR_API uint32_t get_timestamp(void);

// // 通用函数声明
// void delay_ms(uint32_t ms);
// uint32_t get_timestamp(void);



#endif // COMMON_H