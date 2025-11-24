#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include "common.h"
#include "config.h"

#ifdef __cplusplus
extern "C" {
#endif

// MQTT客户端初始化
result_code_t mqtt_client_init(void);

// MQTT连接管理
result_code_t mqtt_connect(void);
void mqtt_disconnect(void);
bool mqtt_is_connected(void);
mqtt_state_t mqtt_get_state(void);

// 数据发布
result_code_t mqtt_publish_sensor_data(const sensor_data_t* data);
result_code_t mqtt_publish_status(const device_status_t* status);

// 周期处理（需要在主循环中调用）
void mqtt_process(void);

// 获取最后错误信息
const char* mqtt_get_last_error(void);

#ifdef __cplusplus
}
#endif

#endif // MQTT_CLIENT_H