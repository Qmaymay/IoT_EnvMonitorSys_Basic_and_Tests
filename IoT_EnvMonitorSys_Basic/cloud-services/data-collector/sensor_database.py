"""
简单的传感器数据库 - 使用SQLite存储历史数据
"""
import sqlite3
import json
from datetime import datetime

class SensorDatabase:
    def __init__(self, db_path="sensor_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                air_quality REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                environment_type TEXT NOT NULL,  # 环境类型:舒适/炎热/潮湿等
                comfort_score REAL NOT NULL,     # 舒适度评分 0-100
                health_risk TEXT,               # 健康风险:无/低/中/高
                suggestions TEXT,               # 改善建议
                analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_sensor_data(self, data):
        """保存传感器数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data (device_id, temperature, humidity, air_quality, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['device_id'], data['temp'], data['hum'], data['air'], data['ts']))
        
        conn.commit()
        conn.close()
    
    def get_recent_data(self, device_id, hours=24):
        """获取最近的数据用于AI分析"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT temperature, humidity, air_quality, timestamp 
            FROM sensor_data 
            WHERE device_id = ? AND datetime(created_at) > datetime('now', ?)
            ORDER BY timestamp DESC
        ''', (device_id, f'-{hours} hours'))
        
        data = cursor.fetchall()
        conn.close()
        
        return [{'temp': row[0], 'hum': row[1], 'air': row[2], 'ts': row[3]} for row in data]