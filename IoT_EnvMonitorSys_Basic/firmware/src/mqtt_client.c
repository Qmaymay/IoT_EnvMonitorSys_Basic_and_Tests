// #include <stdio.h>
// #include <string.h>
// #include <time.h>
// #include "MQTTClient.h"  // 添加Paho MQTT头文件

// // 添加全局MQTT客户端
// static MQTTClient client;
// static int connected = 0;

// result_code_t mqtt_client_init(void) {
//     int rc;
//     MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    
//     printf("[MQTT] Initializing MQTT client...\n");
    
//     // 创建客户端
//     rc = MQTTClient_create(&client, "tcp://localhost:1883", MQTT_CLIENT_ID,
//                           MQTTCLIENT_PERSISTENCE_NONE, NULL);
//     if (rc != MQTTCLIENT_SUCCESS) {
//         set_error("Failed to create MQTT client");
//         return RESULT_ERROR;
//     }
    
//     // 设置连接选项
//     conn_opts.keepAliveInterval = MQTT_KEEPALIVE;
//     conn_opts.cleansession = 1;
    
//     mqtt_ctx.initialized = true;
//     printf("[MQTT] Client initialized successfully\n");
//     return RESULT_OK;
// }

// result_code_t mqtt_connect(void) {
//     if (!mqtt_ctx.initialized) {
//         return RESULT_ERROR;
//     }
    
//     MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
//     conn_opts.keepAliveInterval = MQTT_KEEPALIVE;
//     conn_opts.cleansession = 1;
    
//     printf("[MQTT] Connecting to broker...\n");
    
//     int rc = MQTTClient_connect(client, &conn_opts);
//     if (rc != MQTTCLIENT_SUCCESS) {
//         set_error("Failed to connect to MQTT broker");
//         return RESULT_MQTT_ERROR;
//     }
    
//     connected = 1;
//     mqtt_ctx.state = MQTT_STATE_CONNECTED;
//     printf("[MQTT] Connected successfully\n");
//     return RESULT_OK;
// }

// result_code_t mqtt_publish_sensor_data(const sensor_data_t* data) {
//     // 格式化JSON数据
//     char payload[512];
//     snprintf(payload, sizeof(payload),
//         "{\"device_id\":\"%s\",\"temp\":%.2f,\"hum\":%.2f,\"air\":%.2f,\"ts\":%lu}",
//         DEVICE_ID, data->temperature, data->humidity, data->air_quality, data->timestamp);
    
//     printf("[MQTT] Publishing to topic: %s\n", MQTT_TOPIC_DATA);
//     printf("[MQTT] Payload: %s\n", payload);
    
//     // 使用mosquitto_pub命令行发布
//     char command[1024];
//     snprintf(command, sizeof(command), 
//              "\"C:\\Program Files\\mosquitto\\mosquitto_pub.exe\" -t \"%s\" -m '%s'", 
//              MQTT_TOPIC_DATA, payload);
    
//     printf("[MQTT] Command: %s\n", command);
    
//     int result = system(command);
//     printf("[MQTT] System command returned: %d\n", result);
    
//     if (result == 0) {
//         printf("[MQTT] Message published successfully!\n");
//         return RESULT_OK;
//     } else {
//         printf("[MQTT] Failed to publish message!\n");
//         return RESULT_ERROR;
//     }
// }
// }

#include "common.h"
#include "config.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

// 添加缺失的函数实现
uint32_t get_current_time_ms(void) {
    return (uint32_t)(clock() * 1000 / CLOCKS_PER_SEC);
}

void network_delay_ms(uint32_t ms) {
#ifdef _WIN32
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}

// uint32_t get_timestamp(void) {
//     return (uint32_t)time(NULL);
// }

// 简化的MQTT客户端状态
static bool connected = true;

result_code_t mqtt_client_init(void) {
    printf("[MQTT] Initializing (simplified version)\n");
    return RESULT_OK;
}

result_code_t mqtt_connect(void) {
    printf("[MQTT] Connected (simplified)\n");
    connected = true;
    return RESULT_OK;
}

void mqtt_disconnect(void) {
    printf("[MQTT] Disconnected\n");
    connected = false;
}

bool mqtt_is_connected(void) {
    return connected;
}

result_code_t mqtt_publish_sensor_data(const sensor_data_t* data) {
    if (!connected) {
        return RESULT_MQTT_ERROR;
    }

    char payload[512];
    snprintf(payload, sizeof(payload),
        "{\"device_id\":\"%s\",\"temp\":%.2f,\"hum\":%.2f,\"air\":%.2f,\"ts\":%lu}",
        DEVICE_ID, data->temperature, data->humidity, data->air_quality, data->timestamp);
    
    printf("[MQTT] Publishing to topic: %s\n", MQTT_TOPIC_DATA);
    printf("[MQTT] Payload: %s\n", payload);
    
    // 方法1：使用cmd /c和正确的引号转义
    char command[1024];
    snprintf(command, sizeof(command), 
             "cmd /c \"\"C:\\Program Files\\mosquitto\\mosquitto_pub.exe\" -t \"%s\" -m \"%s\"\"", 
             MQTT_TOPIC_DATA, payload);
    
    printf("[MQTT] Executing command...\n");
    int result = system(command);
    printf("[MQTT] Command result: %d\n", result);
    
    return (result == 0) ? RESULT_OK : RESULT_ERROR;
}


void mqtt_process(void) {
    // 空实现
}

const char* mqtt_get_last_error(void) {
    return "No error";
}

result_code_t mqtt_publish_status(const device_status_t* status) {
    printf("[MQTT] Status publishing not implemented\n");
    return RESULT_OK;
}
