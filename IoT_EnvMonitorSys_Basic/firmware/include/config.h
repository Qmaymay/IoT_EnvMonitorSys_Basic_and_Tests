#ifndef CONFIG_H
#define CONFIG_H

// MQTT配置
#define MQTT_BROKER "localhost"
#define MQTT_PORT 1883
#define MQTT_TOPIC_SENSOR "sensors/data"

// 传感器配置
#define SENSOR_READ_INTERVAL_MS 5000  // 5秒读取一次
#define TEMPERATURE_RANGE_MIN -20.0
#define TEMPERATURE_RANGE_MAX 60.0

// 设备配置
#define MAX_RETRY_COUNT 3
#define WATCHDOG_TIMEOUT_MS 30000

#endif // CONFIG_H