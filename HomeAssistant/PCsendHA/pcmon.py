import requests
import psutil
import time
import subprocess

# Home Assistant API 配置
HA_URL = "http://192.168.31.193:8123/api/states/"  # 替换为你的 Home Assistant 地址
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhYTc0NjE3MDAwYmE0MWI4OTczMjc4ZmE4YzQ1ODI4ZiIsImlhdCI6MTc0MTI2MjE5MSwiZXhwIjoyMDU2NjIyMTkxfQ.xj9prYj9dgZuu0n63yKpxBuFiwlMGmZykHmKMj2zc_0"  # 你的 HA 令牌（请替换）

# 传感器名称（在 Home Assistant 配置中注册）
SENSORS = {
    "cpu": "input_number.voltage_control_gpio1",
    "ram": "input_number.voltage_control_gpio0",
    "gpu": "input_number.voltage_control_gpio4",
    "vram": "input_number.voltage_control_gpio21",
}

# 发送数据到 Home Assistant
def update_sensor(sensor_name, value):
    url = f"{HA_URL}{sensor_name}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "state": value,
        "attributes": {"unit_of_measurement": "%"},
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"Updated {sensor_name}: {value}%")
    else:
        print(f"Failed to update {sensor_name}, Response: {response.text}")

# 获取 GPU 负载（支持 NVIDIA）
def get_gpu_usage():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True
        )
        return int(result.stdout.strip())
    except Exception as e:
        print("NVIDIA SMI not found or error:", e)
        return 0  # 如果没有 NVIDIA GPU，返回 0

# 获取 VRAM 使用率
def get_vram_usage():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True
        )
        used, total = map(int, result.stdout.strip().split(", "))
        return int((used / total) * 100)  # 计算 VRAM 使用率（百分比）
    except Exception as e:
        print("NVIDIA SMI not found or error:", e)
        return 0  # 如果没有 NVIDIA GPU，返回 0

# 获取 CPU 和 RAM 统计数据
def get_system_stats():
    # 计算 CPU 负载（采样 3 次取平均值）
    cpu_samples = [psutil.cpu_percent(interval=0.1) for _ in range(3)]
    cpu_avg = sum(cpu_samples) / len(cpu_samples) * 10  # 计算平均值

    # 获取 RAM 可用百分比
    ram_info = psutil.virtual_memory()
    ram_available = (ram_info.used / ram_info.total) * 100

    # 获取 GPU 和 VRAM 数据
    gpu_usage = get_gpu_usage()
    vram_usage = get_vram_usage()

    return int(cpu_avg), int(ram_available), int(gpu_usage), int(vram_usage)

# 主循环
while True:
    cpu, ram, gpu, vram = get_system_stats()

    update_sensor(SENSORS["cpu"], cpu)
    update_sensor(SENSORS["ram"], ram)
    update_sensor(SENSORS["gpu"], gpu)
    update_sensor(SENSORS["vram"], vram)

    time.sleep(0.5)  # 每 2 秒更新一次数据
