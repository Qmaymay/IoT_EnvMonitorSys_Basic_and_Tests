# simple_collector.py
import json
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import time
import sys

# MQTT配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
# 改为订阅具体设备主题
MQTT_TOPIC = "devices/env_monitor_basic_001/sensor_data"

class SimpleDataCollector:
    def __init__(self):
        print("🔧 Initializing Data Collector...")
        self.setup_database()
        self.setup_mqtt()
    
    def setup_database(self):
        """初始化数据库"""
        try:
            self.conn = sqlite3.connect('sensor_data.db')
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT,
                    temperature REAL,
                    humidity REAL,
                    air_quality REAL,
                    timestamp INTEGER,
                    received_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print("✅ Database initialized at sensor_data.db")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def setup_mqtt(self):
        """设置MQTT客户端"""
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            print("✅ MQTT client setup complete")
        except Exception as e:
            print(f"❌ MQTT setup error: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        """连接回调"""
        print(f"🔗 Connection callback: rc={rc}, flags={flags}")
        if rc == 0:
            print("✅ Connected to MQTT broker successfully!")
            # 订阅设备数据主题
            result = client.subscribe(MQTT_TOPIC)
            print(f"📡 Subscribed to: {MQTT_TOPIC}, result: {result}")
        else:
            error_codes = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier", 
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorised"
            }
            print(f"❌ Failed to connect: {error_codes.get(rc, f'Unknown error {rc}')}")
    
    def on_disconnect(self, client, userdata, rc):
        """断开连接回调"""
        print(f"🔌 Disconnected: rc={rc}")
    
    def save_to_database(self, data):
        """在线程安全的保存数据"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data (device_id, temperature, humidity, air_quality, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (data.get('device_id'), data.get('temp'), data.get('hum'), data.get('air'), data.get('ts')))
            conn.commit()
            conn.close()
            print("💾 Data saved to database successfully!")
            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
        
    
    def on_message(self, client, userdata, msg):
        """接收到MQTT消息回调"""
        try:
            print(f"📨 Raw message received on topic: {msg.topic}")
            payload = msg.payload.decode('utf-8')
            print(f"📦 Payload: {payload}")
            
            data = None
            
            # 方法1：尝试解析标准JSON
            try:
                data = json.loads(payload)
                print("✅ Standard JSON parsed successfully")
            except json.JSONDecodeError as e:
                print(f"⚠️  Standard JSON failed: {e}")
                # 方法2：处理Mosquitto的简化格式 {key:value,key:value}
                print("🔄 Trying Mosquitto format...")
                try:
                    data = self.parse_mosquitto_format(payload)
                    print("✅ Mosquitto format parsed successfully")
                except Exception as e2:
                    print(f"❌ Mosquitto format also failed: {e2}")
                    return
            
            if data:
                print(f"📊 Parsed data: {json.dumps(data, indent=2)}")
                # 保存到数据库
                if self.save_to_database(data):
                    print("💾 Data saved successfully!")
                else:
                    print("❌ Failed to save data")
            else:
                print("❌ No data to save")
                
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            import traceback
            traceback.print_exc()

    def parse_mosquitto_format(self, payload):
        """解析Mosquitto的简化格式 {key:value,key:value}"""
        print(f"🛠️  Parsing Mosquitto format: {payload}")
        
        # 移除花括号和空格
        clean = payload.strip('{}').replace(' ', '')
        print(f"🛠️  Cleaned: {clean}")
        
        # 分割键值对
        pairs = clean.split(',')
        print(f"🛠️  Pairs: {pairs}")
        
        data = {}
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                print(f"🛠️  Processing: {key} => {value}")
                # 尝试转换数值
                try:
                    if '.' in value:
                        data[key] = float(value)
                    else:
                        data[key] = int(value)
                except ValueError:
                    data[key] = value  # 保持字符串
        
        print(f"🛠️  Final data: {data}")
        return data
    
    def start(self):
        """启动数据收集服务"""
        print("🚀 Starting IoT Data Collector...")
        print(f"📍 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"🎯 Topic: {MQTT_TOPIC}")
        
        try:
            print("🔄 Attempting to connect to MQTT broker...")
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("✅ Connect command sent")
            
            # 使用 loop_start 而不是 loop_forever，这样不会阻塞
            self.client.loop_start()
            print("🔄 Loop started")
            
            # 测试：5秒后发送一条测试消息
            import threading
            def send_test():
                time.sleep(3)
                print("🧪 Sending self-test message...")
                self.client.publish("devices/self_test/sensor_data", '{"test": "self_test"}')
        
            threading.Thread(target=send_test).start()
            
            # 保持主线程运行
            while True:
                time.sleep(1)

                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down data collector...")
            self.client.loop_stop()
            self.client.disconnect()
            self.conn.close()

        except Exception as e:
            print(f"❌ Connection error: {e}")

        # except Exception as e:
        #     print(f"❌ Unexpected error: {e}")
        #     import traceback
        #     traceback.print_exc()

if __name__ == "__main__":
    print("=" * 50)
    print("IoT Data Collector - Debug Version")
    print("=" * 50)
    collector = SimpleDataCollector()
    collector.start()