"""
路径解析工具 - 用于跨平台定位构建产物
"""
import platform
import os
from pathlib import Path

class PathResolver:
    """构建产物路径解析器"""
    
    def __init__(self, project_root=None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.firmware_dir = self.project_root / "IoT_EnvMonitorSys_Basic" / "firmware"
        
    def get_library_path(self):
        """获取动态库路径"""
        if platform.system() == "Windows":
            lib_name = "env_monitor.dll"
            lib_dir = self.firmware_dir / "build" / "lib"
        else:
            # Linux 和其他 Unix-like 系统
            lib_name = "libenv_monitor.so"
            lib_dir = self.firmware_dir / "build" / "lib"
        
        lib_path = lib_dir / lib_name
        
        # 如果主库文件不存在，尝试查找其他变体（Linux 符号链接）
        if not lib_path.exists() and platform.system() != "Windows":
            for file in lib_dir.glob("libenv_monitor.so*"):
                if file.is_file() and not file.is_symlink():
                    return file
                elif file.is_symlink():
                    # 返回符号链接指向的实际文件
                    real_path = file.resolve()
                    if real_path.exists():
                        return real_path
        
        return lib_path
    
    def get_executable_path(self):
        """获取可执行文件路径"""
        if platform.system() == "Windows":
            exe_name = "env_monitor_app.exe"
            exe_dir = self.firmware_dir / "build" / "bin" / "Release"
        else:
            exe_name = "env_monitor_app"
            exe_dir = self.firmware_dir / "build" / "bin"
        
        return exe_dir / exe_name
    
    def get_build_artifacts(self):
        """获取所有构建产物信息"""
        lib_path = self.get_library_path()
        exe_path = self.get_executable_path()
        
        return {
            "library": {
                "path": lib_path,
                "exists": lib_path.exists(),
                "is_file": lib_path.is_file() if lib_path.exists() else False
            },
            "executable": {
                "path": exe_path,
                "exists": exe_path.exists(),
                "is_file": exe_path.is_file() if exe_path.exists() else False
            },
            "build_dir": self.firmware_dir / "build",
            "build_dir_exists": (self.firmware_dir / "build").exists()
        }
    
    def validate_paths(self):
        """验证所有路径是否存在"""
        artifacts = self.get_build_artifacts()
        
        print("🔍 构建产物路径验证:")
        print(f"项目根目录: {self.project_root}")
        print(f"固件目录: {self.firmware_dir}")
        
        for artifact_type, info in artifacts.items():
            if artifact_type in ["library", "executable"]:
                status = "✅ 存在" if info["exists"] else "❌ 不存在"
                print(f"{artifact_type}: {info['path']} {status}")
        
        return artifacts

# 创建全局实例
path_resolver = PathResolver()

# 便捷函数
def get_library_path():
    return path_resolver.get_library_path()

def get_executable_path():
    return path_resolver.get_executable_path()

def get_build_artifacts():
    return path_resolver.get_build_artifacts()

if __name__ == "__main__":
    # 测试代码
    artifacts = path_resolver.validate_paths()
    print(f"\n📊 构建状态: {all(artifacts['library']['exists'], artifacts['executable']['exists'])}")
    