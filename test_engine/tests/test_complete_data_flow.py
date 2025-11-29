"""
完整数据流测试 - 从接收到分析的端到端测试
"""
import sys
import os
import json
import time
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'IoT_EnvMonitorSys_Basic', 'cloud-services'))

ai_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'IoT_EnvMonitorSys_Basic', 'cloud_services', 'ai_analyzer')
shared_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'IoT_EnvMonitorSys_Basic', 'cloud_services', 'shared')

sys.path.extend([ai_dir, shared_dir])

def test_complete_data_flow():
    """测试从接收到分析的完整数据流"""
    print("🚀 开始完整数据流测试...")
    
    # 1. 初始化组件
    from database import DatabaseManager
    from real_ai_analyzer import RealAIAnalyzer
    
    db = DatabaseManager(":memory:")  # 使用内存数据库避免污染
    ai = RealAIAnalyzer()
    
    # 2. 模拟传感器数据（相当于MQTT接收到的数据）
    sensor_data = {
        "device_id": "test_sensor_001",
        "temp": 28.5,      # 模拟炎热环境
        "hum": 65.0,
        "air": 85.0, 
        "ts": int(time.time())
    }
    
    print(f" 模拟传感器数据: {json.dumps(sensor_data, indent=2)}")
    
    # 3. 数据存储（相当于data-collector的功能）
    db.save_sensor_data(sensor_data)
    print(" 数据存储成功")
    
    # 4. 验证数据存储
    recent_data = db.get_recent_data("env_monitor_basic_001", 1)
    assert len(recent_data) > 0, "数据存储失败"
    assert recent_data[0]['temp'] == 28.5, "存储的数据不正确"
    print("✅ 数据存储验证通过")
    
    # 5. AI分析（相当于ai-analyzer的功能）
    analysis_result = ai.analyze_with_ai(
        sensor_data["device_id"],
        sensor_data["temp"], 
        sensor_data["hum"],
        sensor_data["air"]
    )
    
    print(f" AI分析结果: {json.dumps(analysis_result, indent=2, ensure_ascii=False)}")
    
    # 6. 验证AI分析结果
    assert "environment_type" in analysis_result, "AI分析缺少环境类型"
    assert "ai_suggestions" in analysis_result, "AI分析缺少建议"
    assert len(analysis_result["ai_suggestions"]) > 0, "AI建议为空"
    
    # 7. 验证针对炎热环境的特定建议
    if "炎热" in analysis_result["environment_type"]:
        assert any("降温" in suggestion or "空调" in suggestion 
                  for suggestion in analysis_result["ai_suggestions"]), "应该有针对炎热的建议"
    
    print("✅ AI分析验证通过")
    
    # 8. 完整流程验证
    print("🎉 完整数据流测试通过！")
    print("   传感器数据 → 存储 → AI分析 → 智能建议")
    
    return True

def test_multiple_data_points():
    """测试多个数据点的处理"""
    from shared.database import DatabaseManager
    from ai_analyzer.real_ai_analyzer import RealAIAnalyzer
    
    db = DatabaseManager(":memory:")
    ai = RealAIAnalyzer()
    
    # 测试不同环境条件
    test_cases = [
        {"temp": 35.0, "hum": 40.0, "air": 70.0, "expected_env": "炎热"},
        {"temp": 15.0, "hum": 85.0, "air": 60.0, "expected_env": "潮湿"}, 
        {"temp": 22.0, "hum": 55.0, "air": 90.0, "expected_env": "舒适"}
    ]
    
    for i, case in enumerate(test_cases):
        data = {
            "device_id": f"test_sensor_{i}",
            "temp": case["temp"],
            "hum": case["hum"],
            "air": case["air"],
            "ts": int(time.time()) + i
        }
        
        # 完整流程
        db.save_sensor_data(data)
        result = ai.analyze_with_ai(data["device_id"], data["temp"], data["hum"], data["air"])
        
        print(f" 测试案例 {i+1}: {case['expected_env']}环境")
        print(f"   结果: {result['environment_type']}")
        assert result['environment_type'] in ["炎热", "潮湿", "舒适", "理想环境"], f"异常环境类型: {result['environment_type']}"
    
    print("✅ 多数据点测试通过")

if __name__ == "__main__":
    test_complete_data_flow()
    test_multiple_data_points()
    print("🎉 所有完整数据流测试通过！")