# shared/database.py - 合并版本
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="sensor_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化两个表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 保持现有的传感器表结构
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                air_quality REAL,
                timestamp INTEGER,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 从sensor_database.py添加AI分析表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                environment_type TEXT NOT NULL,
                comfort_score REAL NOT NULL,
                health_risk TEXT,
                suggestions TEXT,
                analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    
    def save_sensor_data(self, data):
        """保存传感器数据到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data 
            (device_id, temperature, humidity, air_quality, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('device_id'),
            data.get('temp'),
            data.get('hum'), 
            data.get('air'),
            data.get('ts')
        ))
        
        conn.commit()
        conn.close()
        print(f"Data saved: {data['device_id']} at {datetime.now()}")
    

        def get_recent_data(self, device_id: str, hours: int = 24):
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