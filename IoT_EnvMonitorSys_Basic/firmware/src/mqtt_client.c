#include "common.h"
#include "config.h"
#include <stdio.h>
#include <string.h>

// 简化的MQTT发布函数
bool mqtt_publish_sensor_data(const sensor_data_t* data) {
    // 格式化JSON数据
    char payload[256];
    snprintf(payload, sizeof(payload),
        "{\"device_id\":\"%s\",\"temp\":%.2f,\"hum\":%.2f,\"air\":%.2f,\"ts\":%lu}",
        DEVICE_ID, data->temperature, data->humidity, 
        data->air_quality, data->timestamp);
    
    printf("[MQTT] Publishing: %s\n", payload);
    
    // 这里模拟发布成功
    // 实际项目中会调用MQTT客户端库
    return true;
}

// MQTT连接管理
bool mqtt_connect(void) {
    printf("[MQTT] Connecting to %s:%d\n", MQTT_BROKER, MQTT_PORT);
    // 模拟连接成功
    return true;
}

void mqtt_disconnect(void) {
    printf("[MQTT] Disconnected\n");
}