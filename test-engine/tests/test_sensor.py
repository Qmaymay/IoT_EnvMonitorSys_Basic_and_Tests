"""
传感器模块单元测试
"""
import pytest
import ctypes
import os
from pathlib import Path

class TestSensorModule:
    """传感器模块测试"""
    
    def setup_class(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.build_path = self.project_root / "build" / "lib"
        self.dll_path = self.build_path / "env_monitor.dll"
        
    def test_sensor_library_loading(self):
        """测试传感器库加载"""
        if not self.dll_path.exists():
            pytest.skip("动态库文件不存在")
            
        try:
            lib = ctypes.CDLL(str(self.dll_path))
            # 这里可以添加具体的传感器函数测试
            print("✅ 传感器库加载成功")
        except Exception as e:
            pytest.fail(f"传感器库加载失败: {e}")
            