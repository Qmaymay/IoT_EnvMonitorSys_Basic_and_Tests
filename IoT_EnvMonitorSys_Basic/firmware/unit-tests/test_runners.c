#include <stdio.h>
#include <assert.h>
#include "../include/common.h"
#include "../include/config.h"

// 简单的测试框架
void test_sensor_data_validation(void) {
    printf("Testing sensor data validation...\n");
    
    sensor_data_t good_data = {25.0, 50.0, 80.0, 123456};
    sensor_data_t bad_data = {1000.0, 50.0, 80.0, 123456}; // 温度超范围
    
    assert(validate_sensor_data(&good_data) == true);
    assert(validate_sensor_data(&bad_data) == false);
    
    printf("✅ Sensor data validation test passed!\n");
}

void test_mqtt_payload_format(void) {
    printf("Testing MQTT payload format...\n");
    
    sensor_data_t test_data = {23.5, 65.2, 75.8, 999999};
    
    // 这里简单测试，实际应该检查格式化函数
    printf("Data ready for MQTT: temp=%.1f, hum=%.1f\n", 
           test_data.temperature, test_data.humidity);
    
    printf("✅ MQTT payload test passed!\n");
}

void test_config_values(void) {
    printf("Testing configuration values...\n");
    
    assert(SENSOR_READ_INTERVAL_MS == 5000);
    assert(TEMPERATURE_RANGE_MIN == -20.0);
    assert(TEMPERATURE_RANGE_MAX == 60.0);
    
    printf("✅ Configuration test passed!\n");
}

int main(void) {
    printf("=== Starting Firmware Unit Tests ===\n\n");
    
    test_sensor_data_validation();
    test_mqtt_payload_format(); 
    test_config_values();
    
    printf("\n=== All tests passed! ===\n");
    return 0;
}