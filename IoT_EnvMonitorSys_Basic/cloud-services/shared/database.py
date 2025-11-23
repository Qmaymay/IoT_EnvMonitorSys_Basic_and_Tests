import sqlite3
import json
from datetime import datetime

class DatabaseManager:
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
                temperature REAL,
                humidity REAL,
                air_quality REAL,
                timestamp INTEGER,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
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