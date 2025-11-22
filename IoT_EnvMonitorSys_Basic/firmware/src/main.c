#include <stdio.h> 
#include "common.h"
#include "config.h"
#include "sensor_emulator.h"  // 添加这行
#include "mqtt_client.h"      // 添加这行

// 简单的延时函数
void delay_ms(uint32_t ms) {
    // 实际项目中会用RTOS的延时或硬件定时器
    // 这里简单模拟
    for(volatile uint32_t i = 0; i < ms * 1000; i++);
}

// 获取时间戳
uint32_t get_timestamp(void) {
    // 实际项目中从RTC获取
    static uint32_t counter = 0;
    return counter++;
}

int main(void) {
    printf("=== IoT Environment Monitor Started ===\n");
    printf("Device ID: %s\n", DEVICE_ID);
    printf("Firmware Version: %s\n", FIRMWARE_VERSION);
    
    // 初始化MQTT连接
    if (!mqtt_connect()) {
        printf("ERROR: MQTT connection failed!\n");
        return -1;
    }
    
    // 主循环
    while (1) {
        // 读取传感器数据
        sensor_data_t sensor_data = read_sensor_data();
        
        // 验证数据
        if (validate_sensor_data(&sensor_data)) {
            // 发布到MQTT
            if (mqtt_publish_sensor_data(&sensor_data)) {
                printf("Data published successfully\n");
            } else {
                printf("ERROR: Failed to publish data\n");
            }
        } else {
            printf("ERROR: Invalid sensor data\n");
        }
        
        // 等待下一次读取
        delay_ms(SENSOR_READ_INTERVAL_MS);
    }
    
    mqtt_disconnect();
    return 0;
}  