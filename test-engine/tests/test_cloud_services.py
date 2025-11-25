"""
cloud-services核心功能测试
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'IoT_EnvMonitorSys_Basic', 'cloud-services'))

def test_ai_analyzer_integration():
    """测试AI分析器集成"""
    from ai_analyzer.real_ai_analyzer import RealAIAnalyzer
    
    ai = RealAIAnalyzer()
    result = ai.analyze_with_ai("test_device", 25.5, 60.0, 85.0)
    
    assert "environment_type" in result
    assert "ai_suggestions" in result
    print("✅ AI分析器测试通过")

def test_database_integration():
    """测试数据库集成"""
    from shared.database import DatabaseManager
    
    db = DatabaseManager(":memory:")  # 内存数据库，不污染真实数据
    test_data = {
        "device_id": "test_device", 
        "temp": 25.5, 
        "hum": 60.0, 
        "air": 85.0, 
        "ts": 1234567890
    }
    
    db.save_sensor_data(test_data)
    recent_data = db.get_recent_data("test_device", 1)
    
    assert len(recent_data) > 0
    print("✅ 数据库测试通过")

    