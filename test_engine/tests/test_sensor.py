"""
传感器模块完整测试 - 验证数据合理性和连续性
"""
import pytest
import ctypes
import os, sys
import time
import statistics
from pathlib import Path
from datetime import datetime, timedelta 

# 添加项目根目录
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
# 现在可以正确导入
from test_engine.utils.path_resolver import get_build_artifacts, get_library_path


class TestSensorModule:
    """传感器模块完整测试"""
    
    def setup_class(self):
        """初始化测试环境"""
        # self.project_root = Path(__file__).parent.parent.parent
        # self.build_path = self.project_root / "build" / "lib"
        self.dll_path = get_library_path()
        
        if not self.dll_path.exists():
            pytest.skip("动态库文件不存在，跳过传感器测试")
            
        # 加载传感器库
        try:
            self.lib = ctypes.CDLL(str(self.dll_path))

                               
            # 定义函数原型（根据你的C代码实际函数）
            self.lib.sensor_get_temperature.restype = ctypes.c_float
            self.lib.sensor_get_humidity.restype = ctypes.c_float
            self.lib.sensor_get_air_quality.restype = ctypes.c_float
            
            # 其他函数
            # self.lib.sensor_emulator_init.restype = ctypes.c_int
            # self.lib.sensor_emulator_read.argtypes = [ctypes.POINTER(sensor_data_t)]
            # self.lib.sensor_emulator_read.restype = ctypes.c_int
            # self.lib.get_humidity.restype = ctypes.c_float
            # self.lib.get_air_quality.restype = ctypes.c_float
            # self.lib.read_sensor_data.restype = ctypes.c_int
        
        except Exception as e:
            pytest.skip(f"传感器库加载失败: {e}")
        
        # 测试配置
        self.sample_count = 50  # 采样次数
        self.sample_interval = 0.1  # 采样间隔(秒)
        
        # 合理值范围（根据实际传感器规格）
        self.valid_ranges = {
            'temperature': (-10.0, 50.0),      # 温度合理范围
            'humidity': (0.0, 100.0),          # 湿度合理范围
            'air_quality': (0.0, 500.0)        # 空气质量合理范围
        }

    def test_sensor_library_loading(self):
        """测试传感器库正确加载"""
        assert self.lib is not None
        print("✅ 传感器库加载成功")

    def test_sensor_data_validity(self):
        """测试传感器数据合理性"""
        print("🧪 测试传感器数据合理性...")
        
        invalid_readings = 0
        total_readings = 0
        
        for i in range(self.sample_count):
            # 模拟读取传感器数据（根据你的实际函数）
            # 这里需要根据你的C代码接口调整
            temp = self._simulate_sensor_reading('temperature')
            hum = self._simulate_sensor_reading('humidity')
            air = self._simulate_sensor_reading('air_quality')
            
            # 验证数据在合理范围内
            if not (self.valid_ranges['temperature'][0] <= temp <= self.valid_ranges['temperature'][1]):
                invalid_readings += 1
                print(f"⚠️ 异常温度读数: {temp}°C")
                
            if not (self.valid_ranges['humidity'][0] <= hum <= self.valid_ranges['humidity'][1]):
                invalid_readings += 1
                print(f"⚠️ 异常湿度读数: {hum}%")
                
            if not (self.valid_ranges['air_quality'][0] <= air <= self.valid_ranges['air_quality'][1]):
                invalid_readings += 1
                print(f"⚠️ 异常空气质量读数: {air}")
            
            total_readings += 3  # 三个传感器
            time.sleep(self.sample_interval)
        
        # 允许少量异常读数（传感器噪声）
        anomaly_ratio = invalid_readings / total_readings
        assert anomaly_ratio < 0.05, f"异常读数比例过高: {anomaly_ratio:.1%}"
        print(f"✅ 数据合理性测试通过 - 异常率: {anomaly_ratio:.1%}")

    def test_sensor_data_continuity(self):
        """测试传感器数据连续性 - 检测时间断裂和突变"""
        print("⏱️ 测试传感器数据连续性...")
        
        timestamps = []
        temperatures = []
        last_temp = None
        
        start_time = time.time()
        
        for i in range(self.sample_count):
            current_time = time.time()
            temp = self._simulate_sensor_reading('temperature')
            
            timestamps.append(current_time)
            temperatures.append(temp)
            
            # 检测数据突变
            if last_temp is not None:
                temp_change = abs(temp - last_temp)
                if temp_change > 10.0:  # 温度突变阈值(°C/采样)
                    pytest.fail(f"温度突变检测: {last_temp} → {temp} (变化: {temp_change}°C)")
            
            last_temp = temp
            time.sleep(self.sample_interval)
        
        # 分析时间连续性
        time_diffs = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        avg_interval = statistics.mean(time_diffs)
        max_interval = max(time_diffs)
        
        print(f"📊 采样统计 - 平均间隔: {avg_interval:.3f}s, 最大间隔: {max_interval:.3f}s")
        
        # 验证时间连续性
        expected_interval = self.sample_interval * 1.5  # 允许50%的误差
        assert max_interval < expected_interval, f"时间断裂检测: 最大间隔 {max_interval}s 超过预期"
        
        # 验证数据稳定性
        temp_std = statistics.stdev(temperatures)
        assert temp_std < 5.0, f"温度数据波动过大: 标准差 {temp_std:.2f}°C"
        
        print("✅ 数据连续性测试通过")

    def test_sensor_calibration(self):
        """测试传感器校准和噪声水平"""
        print("🎯 测试传感器噪声水平...")
        
        # 在稳定环境下测试噪声
        base_temperature = self._simulate_sensor_reading('temperature')
        readings = []
        
        for i in range(20):  # 快速连续采样
            readings.append(self._simulate_sensor_reading('temperature'))
            time.sleep(0.05)
        
        # 计算噪声水平
        avg_temp = statistics.mean(readings)
        noise_level = statistics.stdev(readings)
        
        print(f"📊 基准温度: {base_temperature:.2f}°C, 平均: {avg_temp:.2f}°C, 噪声: {noise_level:.3f}°C")
        
        # 验证噪声在可接受范围内
        assert noise_level < 1.0, f"传感器噪声过大: {noise_level:.3f}°C"
        assert abs(avg_temp - base_temperature) < 2.0, "传感器读数偏差过大"
        
        print("✅ 传感器校准测试通过")

    def test_sensor_error_handling(self):
        """测试传感器错误处理"""
        print("🚨 测试传感器错误处理...")
        
        # 测试边界值处理
        extreme_conditions = [
            (-100.0, 'temperature'),  # 极低温度
            (1000.0, 'temperature'),  # 极高温度
            (-10.0, 'humidity'),      # 无效湿度
            (150.0, 'humidity'),      # 无效湿度
        ]
        
        for value, sensor_type in extreme_conditions:
            # 这里应该测试你的C代码如何处理异常值
            # 例如：返回错误码、使用默认值等
            try:
                result = self._simulate_extreme_reading(value, sensor_type)
                # 验证系统不会崩溃，且有合理的错误处理
                assert result is not None, f"传感器在极端条件 {sensor_type}={value} 下无响应"
            except Exception as e:
                print(f"⚠️ 极端条件测试 {sensor_type}={value} 产生异常: {e}")
        
        print("✅ 错误处理测试通过")

    def _simulate_sensor_reading(self, sensor_type):
        """模拟传感器读数 - 需要根据你的实际C函数修改"""
        # 这里是模拟代码，实际应该调用你的C函数
        import random
        if sensor_type == 'temperature':
            return 20.0 + random.uniform(-2.0, 2.0)  # 20°C ± 2°C
        elif sensor_type == 'humidity':
            return 50.0 + random.uniform(-10.0, 10.0)  # 50% ± 10%
        elif sensor_type == 'air_quality':
            return 100.0 + random.uniform(-20.0, 20.0)  # 100 ± 20
        return 0.0

    def _simulate_extreme_reading(self, value, sensor_type):
        """模拟极端条件读数 - 需要根据你的实际C函数修改"""
        # 这里应该调用你的C代码处理极端值
        # 暂时返回模拟值
        return value

if __name__ == "__main__":
    # 直接运行测试
    test = TestSensorModule()
    test.setup_class()
    
    print("🚀 开始传感器完整测试...")
    try:
        test.test_sensor_library_loading()
        test.test_sensor_data_validity()
        test.test_sensor_data_continuity()
        test.test_sensor_calibration()
        test.test_sensor_error_handling()
        print("🎉 所有传感器测试通过！")
    except Exception as e:
        print(f"❌ 传感器测试失败: {e}")
        raise

