# IoT_EnvMonitorSys_Basic/firmware/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)

# 项目名称和语言
project(IoT_EnvMonitor C)

# 设置C标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 编译选项
if(MSVC)
    add_compile_options(/W3)
else()
    add_compile_options(-Wall -Wextra -g)
endif()

# 包含头文件目录
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# 🆕 只设置运行时和库输出目录，删除归档目录
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/build/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/build/lib)

# 可执行文件 - 主设备程序
add_executable(env_monitor
    src/main.c
    src/sensor_emulator.c  
    src/mqtt_client.c
)

# 动态库 - 供Python测试调用
add_library(env_monitor_shared SHARED
    src/sensor_emulator.c
    src/mqtt_client.c
)

# 设置库的属性
set_target_properties(env_monitor_shared PROPERTIES
    OUTPUT_NAME "env_monitor"
    VERSION 1.0.0
    SOVERSION 1
)

# 设置可执行文件输出名称，避免与库文件冲突
set_target_properties(env_monitor PROPERTIES
    OUTPUT_NAME "env_monitor_app"
)

message(STATUS "=== IoT Environment Monitor CMake配置 ===")
message(STATUS "项目名称: ${PROJECT_NAME}")
message(STATUS "输出目录: ${CMAKE_BINARY_DIR}/lib")
message(STATUS "生成目标:")
message(STATUS "  env_monitor_app     - 设备可执行程序")
message(STATUS "  env_monitor         - 设备动态库")