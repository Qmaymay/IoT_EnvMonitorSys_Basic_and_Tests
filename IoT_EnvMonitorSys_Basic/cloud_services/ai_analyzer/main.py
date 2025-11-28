import sys
import os
from datetime import datetime, timedelta
import sqlite3

# 添加shared目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir = os.path.join(current_dir, '..', 'shared')
sys.path.insert(0, shared_dir)

from real_ai_analyzer import RealAIAnalyzer
# IDE可能会显示"无法解析导入"，但运行时正常
from database import DatabaseManager


def diagnose_database(db_path):
    """数据库诊断工具 - 仅在需要时调用"""
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 数据库诊断报告:")
        print("=" * 40)
        
        # 1. 表信息
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 数据表: {tables}")
        
        # 2. 数据统计
        if 'sensor_data' in tables:
            cursor.execute("SELECT COUNT(*) FROM sensor_data")
            total = cursor.fetchone()[0]
            print(f"📊 传感器数据总数: {total} 条")
            
            cursor.execute("SELECT device_id, COUNT(*) FROM sensor_data GROUP BY device_id")
            devices = cursor.fetchall()
            print(f"📱 设备分布: {dict(devices)}")
            
            if total > 0:
                cursor.execute("SELECT MIN(received_at), MAX(received_at) FROM sensor_data")
                time_range = cursor.fetchone()
                print(f"⏰ 数据时间范围: {time_range[0]} 到 {time_range[1]}")
        
        print("=" * 40)
        conn.close()
        
    except Exception as e:
        print(f"❌ 诊断失败: {e}")

def main():

    # 明确指定数据库路径，和接收器使用同一个
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shared_dir = os.path.join(current_dir, '..', 'shared')
    
    # 使用与database.py相同的数据库路径
    shared_db_path = os.path.join(shared_dir, "sensor_data.db")
    print(f"📁 使用数据库文件: {shared_db_path}")
    print(f"📁 数据库文件存在: {os.path.exists(shared_db_path)}")
    
    # 初始化时指定数据库路径
    db_manager = DatabaseManager(db_path=shared_db_path)

     # 添加调试：查看真实数据量
    conn = sqlite3.connect(shared_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sensor_data")
    total_count = cursor.fetchone()[0]
    print(f"📊 数据库中总数据量: {total_count} 条")
    conn.close()

    ai_analyzer = RealAIAnalyzer()
    
    device_id = "test_device_001"  # 使用与测试数据相同的设备ID
    
    try:
        # 🎯 查询所有设备的数据
        conn = sqlite3.connect(shared_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT device_id, temperature, humidity, air_quality, timestamp 
            FROM sensor_data 
            ORDER BY id DESC LIMIT 10
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        recent_data = [{'temp': row[1], 'hum': row[2], 'air': row[3], 'ts': row[4]} for row in data]
        
        print(f"📊 查询到的数据条数: {len(recent_data)}")
        
        # 显示设备分布
        print("🔍 最新数据的设备分布:")
        for i, row in enumerate(data):
            print(f"   {i+1}. 设备: {row[0]}, 温度: {row[1]}°C")
        
        # 使用最新数据进行分析
        if recent_data:
            latest_data = recent_data[0]
            temp = latest_data['temp']
            hum = latest_data['hum'] 
            air = latest_data['air']
            
            print(f"\n🎯 使用最新数据进行分析:")
            print(f"   温度: {temp}°C, 湿度: {hum}%, 空气质量: {air}%")
            
            # AI分析
            result = ai_analyzer.analyze_with_ai("current_device", temp, hum, air)
            
            print("\n🤖 AI分析结果:")
            print(f"   环境类型: {result['environment_type']}")
            print(f"   预测置信度: {result['prediction_confidence']}")
            print(f"   异常分数: {result['anomaly_score']}")
            print("   AI建议:")
            for suggestion in result['ai_suggestions']:
                print(f"     • {suggestion}")
        
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")


    # 使用方式：只在发现问题时调用
    if not recent_data:
        print("❌ 未找到数据，启动诊断...")
        diagnose_database(shared_db_path)
        print("💡 建议: 检查传感器数据写入或设备ID匹配")
        return

if __name__ == "__main__":
    main()
    