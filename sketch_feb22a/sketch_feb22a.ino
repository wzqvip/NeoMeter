#include <Arduino.h>
#include "driver/ledc.h"  // 需要包含 LEDC 头文件

// 目标输出 GPIO
const int pwm_pins[] = {1, 0, 5, 21};
const int pwm_channels[] = {LEDC_CHANNEL_0, LEDC_CHANNEL_1, LEDC_CHANNEL_2, LEDC_CHANNEL_3};

// PWM 配置
#define LEDC_TIMER          LEDC_TIMER_0
#define LEDC_MODE           LEDC_LOW_SPEED_MODE
#define LEDC_FREQUENCY      5000 // 5kHz
#define LEDC_RESOLUTION     LEDC_TIMER_12_BIT // 12-bit 分辨率（0~4095）

void setup() {
    Serial.begin(115200); // 初始化串口
    
    // 配置 LEDC Timer
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,
        .duty_resolution = LEDC_RESOLUTION,
        .timer_num = LEDC_TIMER,
        .freq_hz = LEDC_FREQUENCY,
        .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);

    // 初始化 PWM 通道
    for (int i = 0; i < 4; i++) {
        ledc_channel_config_t ledc_channel = {
            .gpio_num = pwm_pins[i],
            .speed_mode = LEDC_MODE,
            .channel = (ledc_channel_t)pwm_channels[i],
            .intr_type = LEDC_INTR_DISABLE,
            .timer_sel = LEDC_TIMER,
            .duty = 0, // 初始占空比 0
            .hpoint = 0
        };
        ledc_channel_config(&ledc_channel);
    }
}

void loop() {
    static String inputString = "";
    while (Serial.available()) {
        char c = Serial.read();
        if (c == ';') {  // 解析结束符
            processInput(inputString);
            inputString = "";
        } else {
            inputString += c;
        }
    }
}

// 解析数据并输出 PWM
void processInput(String data) {
    int values[4] = {0};
    int index = 0;
    char *token = strtok((char *)data.c_str(), ",");

    while (token != NULL && index < 4) {
        values[index] = constrain(atoi(token), 0, 100);
        token = strtok(NULL, ",");
        index++;
    }

    // 映射 0~100 到 PWM (0~4095 = 0~3V)
    for (int i = 0; i < 4; i++) {
        int duty = map(values[i], 0, 100, 0, 4095);
        ledc_set_duty(LEDC_MODE, (ledc_channel_t)pwm_channels[i], duty);
        ledc_update_duty(LEDC_MODE, (ledc_channel_t)pwm_channels[i]);
    }
}
