#ifndef CONFIG_H
#define CONFIG_H

// 设备配置
#define DEVICE_ID "env_monitor_basic_001"
#define FIRMWARE_VERSION "1.0.0"
#define FEATURE_SET "basic-loop"

// 传感器配置
#define SENSOR_READ_INTERVAL_MS 5000  // 5秒读取一次
#define TEMPERATURE_RANGE_MIN -20.0
#define TEMPERATURE_RANGE_MAX 60.0

// MQTT配置
#define MQTT_BROKER "localhost"  // 或实际的MQTT服务器地址
#define MQTT_PORT 1883
#define MQTT_CLIENT_ID "env_monitor_" DEVICE_ID
#define MQTT_KEEPALIVE 60
#define MQTT_QOS 1


#define MQTT_TOPIC_SENSOR "sensors/data"

#define MQTT_TOPIC_DATA "devices/" DEVICE_ID "/sensor_data"
#define MQTT_TOPIC_STATUS "devices/" DEVICE_ID "/status"
#define MQTT_TOPIC_COMMAND "devices/" DEVICE_ID "/command"



// 连接重试配置
#define MAX_RETRY_COUNT 3
#define WATCHDOG_TIMEOUT_MS 30000

#endif // CONFIG_H