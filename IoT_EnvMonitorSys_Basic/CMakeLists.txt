# IoT_EnvMonitorSys_Basic/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(IoT_EnvMonitorSys_Basic)

# 添加固件子项目
add_subdirectory(firmware)

message(STATUS "IoT环境监测系统 - 被测工程")
message(STATUS "固件目录: ${CMAKE_CURRENT_SOURCE_DIR}/firmware")