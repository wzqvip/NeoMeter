# **NeoMeter - ESP32-C3 Mechanical Gauge**

**Lightweight, quiet, fast-response mechanical gauge.**

NeoMeter is a **programmable mechanical gauge system** that leverages the **ESP32-C3** to drive analog needle meters (such as current gauges) using **PWM-based voltage control**.

This project can function in two modes:

1. **Serial Mode (PC Monitoring)** - Reads CPU, RAM, GPU, and VRAM utilization from a computer and maps them to **0-3V outputs** to drive gauges.
2. **Home Assistant Mode** - Integrates with **Home Assistant** for smart home applications, allowing users to control gauge values via a UI.

---

## **🛠️ Hardware**

### **Recommended Analog Gauge Setup**

- **5mA gauge**
- **Two 300Ω resistors in series**
- **Driven using ESP32-C3's PWM 0-3V output**

| **Gauge Type**       | **Connection** |
| -------------------------- | -------------------- |
| **CPU Usage Meter**  | GPIO0                |
| **RAM Usage Meter**  | GPIO1                |
| **GPU Usage Meter**  | GPIO5                |
| **VRAM Usage Meter** | GPIO21               |

### **Example Setup**

![Gauge Setup](image/README/1740229823374.png)

*Works well with 5mA gauges, using two 300Ω resistors in series to achieve 0-3V PWM control.*

---

# **1️⃣ Serial Mode (PC Monitoring)**

**Purpose:** Reads system resource usage (**CPU, RAM, GPU, VRAM**) and maps the data to **mechanical needle gauges** using PWM.

## **💾 Setup (PC Side)**

### **1. Install Dependencies**

Run the following command to install required Python libraries:

```sh
pip install psutil serial gputil
```

### **2. Run the PC Monitoring Script**

Modify `SERIAL_PORT` according to your system (`COMx` for Windows, `/dev/ttyUSBx` for Linux/macOS), then run:

```sh
python Serial_PCmon/pc_monitor.py
```

### **3. Expected Serial Output**

```sh
Sent: 85,60,80,50;
Sent: 82,55,75,45;
```

- **85** → CPU Available (CPU Load = 15%)
- **60** → RAM Available
- **80** → GPU Available (GPU Load = 20%)
- **50** → VRAM Available

### **🔌 Wiring**

| PC Resource          | ESP32-C3 GPIO | Gauge Label |
| -------------------- | ------------- | ----------- |
| **CPU Load**   | GPIO0         | CPU Gauge   |
| **RAM Usage**  | GPIO1         | RAM Gauge   |
| **GPU Load**   | GPIO5         | GPU Gauge   |
| **VRAM Usage** | GPIO21        | VRAM Gauge  |

---

## **📡 ESP32-C3 Firmware (Serial Mode)**

### **Upload `sketch_feb22a.ino` to ESP32-C3**

Use **Arduino IDE** or **PlatformIO** to flash the firmware.

### **ESP32 Features**

✅ **Reads serial data (e.g., `85,60,80,50;`)**
✅ **Maps `0-100%` utilization to `PWM (0-3V)`**
✅ **Outputs PWM signals to control analog meters**

---

# **2️⃣ Home Assistant Mode (ESPHome)**

**Purpose:** Allows gauge control through **Home Assistant**, integrating with smart home automation.

### **🏠 Home Assistant Integration**

NeoMeter can be controlled remotely via **Home Assistant** UI sliders. The sliders adjust **PWM output**, setting the needle gauge position.

### **🔌 Wiring**

| Home Assistant Entity      | ESP32-C3 GPIO | Gauge Label |
| -------------------------- | ------------- | ----------- |
| `voltage_control_gpio0`  | GPIO0         | Gauge 1     |
| `voltage_control_gpio1`  | GPIO1         | Gauge 2     |
| `voltage_control_gpio5`  | GPIO5         | Gauge 3     |
| `voltage_control_gpio21` | GPIO21        | Gauge 4     |

### **⚙️ ESPHome Configuration (`esp32-c3-gauge.yaml`)**

```yaml
esphome:
  name: esp32-c3-gauge
  friendly_name: ESP32-C3-Gauge
  board: esp32-c3-devkitm-1
  platform: ESP32

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
    ssid: "ESP32-C3-Gauge Fallback"
    password: "backup123"

logger:

api:
  encryption:
    key: "lxETubxQ14a51dnMBCWvpFRJ5Ilswsv21MpEk9zAfCM="

ota:
  password: "439b3e036c6b235c7362e925fd92feb7"

number:
  - platform: homeassistant
    entity_id: input_number.voltage_control_gpio0
    id: ha_voltage_gpio0
    on_value:
      then:
        - lambda: |-
            float duty_cycle = x / 100.0;
            id(pwm_output_gpio0).set_level(duty_cycle);

  - platform: homeassistant
    entity_id: input_number.voltage_control_gpio1
    id: ha_voltage_gpio1
    on_value:
      then:
        - lambda: |-
            float duty_cycle = x / 100.0;
            id(pwm_output_gpio1).set_level(duty_cycle);

  - platform: homeassistant
    entity_id: input_number.voltage_control_gpio5
    id: ha_voltage_gpio5
    on_value:
      then:
        - lambda: |-
            float duty_cycle = x / 100.0;
            id(pwm_output_gpio5).set_level(duty_cycle);

  - platform: homeassistant
    entity_id: input_number.voltage_control_gpio21
    id: ha_voltage_gpio21
    on_value:
      then:
        - lambda: |-
            float duty_cycle = x / 100.0;
            id(pwm_output_gpio21).set_level(duty_cycle);

output:
  - platform: ledc
    pin: GPIO0
    frequency: 5000Hz
    id: pwm_output_gpio0

  - platform: ledc
    pin: GPIO1
    frequency: 5000Hz
    id: pwm_output_gpio1

  - platform: ledc
    pin: GPIO5
    frequency: 5000Hz
    id: pwm_output_gpio5

  - platform: ledc
    pin: GPIO21
    frequency: 5000Hz
    id: pwm_output_gpio21
```

### **🏠 Controlling the Gauge in Home Assistant**

1. Open **Home Assistant UI**
2. Navigate to **Developer Tools > States**
3. Adjust the **input_number.voltage_control_gpioX** sliders

Each slider **directly sets the PWM output level**, controlling the gauge needle position.

---

# **🛠️ Troubleshooting**

| Issue                        | Solution                                         |
| ---------------------------- | ------------------------------------------------ |
| No serial output in PC mode  | Check `SERIAL_PORT`, ensure ESP32 is connected |
| Needle not moving            | Verify PWM output voltage using a multimeter     |
| Home Assistant not detecting | Check WiFi settings and ESPHome integration      |

---

# **📌 Future Improvements**

- **WiFi Data Streaming** - Stream PC resource usage over MQTT instead of Serial
- **Multiple Meter Support** - Expand to support more gauges with **I²C DAC**
- **OLED Display** - Show resource usage alongside gauges

---

# **📢 Credits**

💡 **Author:** _Your Name_
📅 **Date:** February 2025
🚀 **Inspired by:** Mechanical gauges & Home Automation

Enjoy your **ESP32-C3-powered analog gauge!** 🕹️⚙️📊
