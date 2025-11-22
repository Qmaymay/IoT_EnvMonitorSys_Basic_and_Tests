# 编译器设置
CC = gcc
CFLAGS = -I./include -Wall -Wextra -std=c99 -g
LDFLAGS = -lm

# 源文件
SRC_DIR = src
SRC = $(wildcard $(SRC_DIR)/*.c)

# 目标文件
OBJ_DIR = build
OBJ = $(SRC:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# 可执行文件
TARGET = $(OBJ_DIR)/env_monitor

# 默认目标
all: $(TARGET)

# 链接可执行文件
$(TARGET): $(OBJ)
	@mkdir -p $(OBJ_DIR)
	$(CC) -o $@ $^ $(LDFLAGS)
	@echo "Build successful: $(TARGET)"

# 编译源文件
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# 清理构建文件
clean:
	rm -rf $(OBJ_DIR)
	@echo "Clean complete"

# 运行程序
run: $(TARGET)
	./$(TARGET)

# 调试运行
debug: $(TARGET)
	gdb ./$(TARGET)

.PHONY: all clean run debug


# 运行单元测试
test: $(TARGET)
	@echo "Running unit tests..."
	$(CC) $(CFLAGS) -o $(OBJ_DIR)/test_runner unit-tests/test_runners.c $(SRC_DIR)/sensor_emulator.c $(LDFLAGS)
	./$(OBJ_DIR)/test_runner

# 编译并运行
all-test: clean all test