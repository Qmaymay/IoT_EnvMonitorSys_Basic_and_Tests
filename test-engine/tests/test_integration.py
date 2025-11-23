"""
IoT环境监测系统 - 集成测试
测试设备程序与数据收集服务的完整数据流
"""
import pytest
import json
import time
import threading
import paho.mqtt.client as mqtt
from pathlib import Path
import subprocess
import sys

class TestIoTIntegration:
    """集成测试类"""
    
    def setup_class(self):
        """测试类初始化"""
        self.project_root = Path(__file__).parent.parent.parent
        self.firmware_path = self.project_root / "IoT_EnvMonitorSys_Basic" / "firmware"
        self.build_path = self.project_root / "build" / "lib"
        
        # 🆕 使用现有变量构建路径
        self.exe_path = self.firmware_path / "build" / "bin" / "Release" / "env_monitor_app.exe"
        self.dll_path = self.firmware_path / "build" / "bin" / "Release" / "env_monitor.dll"
        
        print(f"项目根目录: {self.project_root}")
        print(f"固件路径: {self.firmware_path}")
        print(f"构建路径: {self.build_path}")
        
        # MQTT配置
        self.mqtt_broker = "localhost"
        self.mqtt_port = 1883
        self.test_topic = "devices/test_device/sensor_data"
        
        # 测试数据收集
        self.received_messages = []
        self.mqtt_connected = False

    def test_build_output_exists(self):
        """测试构建输出文件是否存在"""
        exe_file = self.build_path / "env_monitor_app.exe"
        dll_file = self.build_path / "env_monitor.dll"
        
        assert exe_file.exists(), f"可执行文件不存在: {exe_file}"
        assert dll_file.exists(), f"动态库文件不存在: {dll_file}"
        
        print(f"✅ 可执行文件: {exe_file}")
        print(f"✅ 动态库文件: {dll_file}")

    def test_executable_runs(self):
        """测试可执行文件能够运行"""
        exe_path = self.build_path / "env_monitor_app.exe"
        
        # 启动进程（不等待完成）
        process = subprocess.Popen(
            [str(exe_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 让程序运行几秒钟
        time.sleep(3)
        
        # 终止进程
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            
        # 检查是否有输出（表明程序正常启动）
        stdout, stderr = process.communicate()
        assert "IoT Environment Monitor" in stdout or "Sensor emulator initialized" in stdout
        print("✅ 可执行文件正常启动")

    def test_dynamic_library_loading(self):
        """测试动态库加载"""
        try:
            import ctypes
            dll_path = self.build_path / "env_monitor.dll"
            lib = ctypes.CDLL(str(dll_path))
            
            # 测试库中的函数
            # 注意：需要根据实际导出函数来测试
            print("✅ 动态库加载成功")
            
        except Exception as e:
            pytest.fail(f"动态库加载失败: {e}")

    def test_mqtt_communication(self):
        """测试MQTT通信"""
        
        def on_connect(client, userdata, flags, rc):
            self.mqtt_connected = True
            client.subscribe(self.test_topic)
            
        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode('utf-8')
                self.received_messages.append({
                    'topic': msg.topic,
                    'payload': payload,
                    'timestamp': time.time()
                })
                print(f"📨 收到测试消息: {payload}")
            except Exception as e:
                print(f"❌ 消息处理错误: {e}")
        
        # 启动MQTT订阅者
        subscriber = mqtt.Client()
        subscriber.on_connect = on_connect
        subscriber.on_message = on_message
        
        try:
            subscriber.connect(self.mqtt_broker, self.mqtt_port, 60)
            subscriber.loop_start()
            
            # 等待连接
            time.sleep(2)
            assert self.mqtt_connected, "MQTT连接失败"
            
            # 发布测试消息
            publisher = mqtt.Client()
            publisher.connect(self.mqtt_broker, self.mqtt_port, 60)
            
            test_message = {
                "device_id": "test_device",
                "temp": 25.5,
                "hum": 60.0,
                "air": 75.0,
                "ts": int(time.time())
            }
            
            publisher.publish(self.test_topic, json.dumps(test_message))
            publisher.disconnect()
            
            # 等待消息接收
            time.sleep(2)
            
            assert len(self.received_messages) > 0, "未收到MQTT消息"
            received_data = json.loads(self.received_messages[0]['payload'])
            assert received_data['device_id'] == 'test_device'
            
            print("✅ MQTT通信测试通过")
            
        finally:
            subscriber.loop_stop()
            subscriber.disconnect()

    def test_sensor_data_format(self):
        """测试传感器数据格式"""
        # 这里可以测试数据格式验证
        valid_data = {
            "device_id": "test_device",
            "temp": 25.5,
            "hum": 60.0, 
            "air": 75.0,
            "ts": int(time.time())
        }
        
        # 验证必需字段
        required_fields = ['device_id', 'temp', 'hum', 'air', 'ts']
        for field in required_fields:
            assert field in valid_data, f"缺少必需字段: {field}"
            
        # 验证数据类型
        assert isinstance(valid_data['temp'], (int, float))
        assert isinstance(valid_data['hum'], (int, float))
        assert isinstance(valid_data['air'], (int, float))
        assert isinstance(valid_data['ts'], int)
        
        print("✅ 传感器数据格式验证通过")

if __name__ == "__main__":
    # 直接运行测试
    test = TestIoTIntegration()
    test.setup_class()
    
    print("🚀 开始运行集成测试...")
    
    try:
        test.test_build_output_exists()
        test.test_executable_runs()
        test.test_dynamic_library_loading()
        test.test_sensor_data_format()
        test.test_mqtt_communication()
        print("🎉 所有集成测试通过！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        raise

