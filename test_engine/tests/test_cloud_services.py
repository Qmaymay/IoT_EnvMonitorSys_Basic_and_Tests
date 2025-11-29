# -*- coding: utf-8 -*-
"""
cloud-services核心功能测试
"""
import sys
import os
from pathlib import Path

# 集中定义所有路径
project_root = Path(__file__).parent.parent.parent
firmware_dir = project_root / "IoT_EnvMonitorSys_Basic" / "firmware"
cloud_services_dir = project_root / "IoT_EnvMonitorSys_Basic" / "cloud_services"

# 添加到Python路径
sys.path.extend([
    str(cloud_services_dir / "ai_analyzer"),
    str(cloud_services_dir / "shared"),
    str(firmware_dir / "utils")  # 如果有utils目录
])

# 现在可以导入
try:
    from path_resolver import get_build_artifacts
    # 或者其他模块
except ImportError as e:
    print(f"导入警告: {e}")
    # 回退到硬编码
# 现在两个都可以导入
from real_ai_analyzer import RealAIAnalyzer
from database import DatabaseManager  # 注意：是 database，不是 shared.database


def test_ai_analyzer_integration():
    """测试AI分析器集成"""
    # from ai_analyzer.real_ai_analyzer import RealAIAnalyzer
    
    ai = RealAIAnalyzer()
    result = ai.analyze_with_ai("test_device", 25.5, 60.0, 85.0)
    
    assert "environment_type" in result
    assert "ai_suggestions" in result
    print("✅ AI分析器测试通过")


if __name__ == "__main__":
    print("开始运行cloud-services测试...")
    test_ai_analyzer_integration()
    print("所有测试完成！")
