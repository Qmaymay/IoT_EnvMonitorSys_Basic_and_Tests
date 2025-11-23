# 总项目根目录的CMakeLists.txt
cmake_minimum_required(VERSION 3.10)

# 总项目名称
project(IoT_EnvMonitorSys_Complete)

# 设置C标准
set(CMAKE_C_STANDARD 11)

# 添加子项目
add_subdirectory(IoT_EnvMonitorSys_Basic)

# 可选：添加测试工程
# add_subdirectory(test-engine)

message(STATUS "==========================================")
message(STATUS "   IoT环境监测系统 - 完整项目构建")
message(STATUS "==========================================")
message(STATUS "可用目标:")
message(STATUS "  env_monitor      - 设备可执行程序")
message(STATUS "  env_monitor_shared - 设备动态库")
message(STATUS "  env_monitor_static - 设备静态库")
message(STATUS "==========================================")