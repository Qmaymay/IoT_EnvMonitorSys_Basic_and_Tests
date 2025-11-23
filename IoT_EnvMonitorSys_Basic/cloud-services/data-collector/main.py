import json
import time
import paho.mqtt.client as mqtt
from shared.database import DatabaseManager

# 配置信息
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "devices/+/sensor_data"

class DataCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.mqtt_client = mqtt.Client()
        
        # 设置MQTT回调函数
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        """MQTT连接成功回调"""
        if rc == 0:
            print("✅ Connected to MQTT broker successfully!")
            # 订阅设备数据主题
            client.subscribe(MQTT_TOPIC)
            print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
        else:
            print(f"❌ Failed to connect, return code {rc}")
    
    def on_message(self, client, userdata, msg):
        """接收到MQTT消息回调"""
        try:
            # 解析JSON数据
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            
            print(f"📨 Received message from topic: {msg.topic}")
            print(f"📊 Data: {json.dumps(data, indent=2)}")
            
            # 保存到数据库
            self.db.save_sensor_data(data)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    def start(self):
        """启动数据收集服务"""
        print("🚀 Starting IoT Data Collector...")
        print(f"📍 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        
        try:
            # 连接MQTT代理
            self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            
            # 启动网络循环（阻塞调用）
            print("🔄 Starting network loop...")
            self.mqtt_client.loop_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down data collector...")
            self.mqtt_client.disconnect()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    collector = DataCollector()
    collector.start()