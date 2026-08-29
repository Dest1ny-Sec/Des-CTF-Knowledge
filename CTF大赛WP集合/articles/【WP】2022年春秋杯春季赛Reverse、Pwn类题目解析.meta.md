---
title: 【WP】2022年春秋杯春季赛 Reverse、Pwn 类题目解析
contest: 春秋杯
year: 2022
difficulty: medium
vuln_type: reverse
tags: [QMK-firmware, keyboard-combo, process_combo_event, keymaps, layer-keycode, KC_TRANSPARENT-inherit, rand-LCG, enc-1CTED8IL]
attack_chain: babyqmk 搜字符串找 qmk_firmware + 找 process_combo_event + 提取 key_combos/CHUNQIU 激活 Combo_1/GAME 激活 Combo_2 切 Layer/提取 keymaps 3 个 Layer 0-9A-Z 不同/formatLayer + buildLayerMap 处理 KC_TRANSPARENT 继承上层/SEED=0 LC(214013, +2531011) rand 生成表/keycodeToKey 映射查表还原 enc="1CTED8IL-BIMM-SMFP-HOKP-HOIDRZL4W6KR"
key_payload: 加密 enc="1CTED8IL-BIMM-SMFP-HOKP-HOIDRZL4W6KR"  SEED=0  rand 公式 214013*x + 2531011
one_liner: 2022 春秋杯春季赛 Reverse/Pwn 2 题 WP，QMK 键盘固件逆向 + Layer keycode 继承 + LCG 还原。
lesson: QMK 是开源键盘固件，组合键 (Combo) 触发 process_combo_event；KC_TRANSPARENT (1) 继承上一层 keycode 是 QMK 关键特性；LCG SEED=0 起始 + 0x7fff 掩码是经典伪随机。
quality: high
---

# 【WP】2022年春秋杯春季赛 Reverse、Pwn 类题目解析

## 概览
2022 春秋杯春季赛 2 道题 WP：babyqmk (QMK 固件) + 1 道 Pwn。

## babyqmk (Reverse)

### 关键词
- `qmk_firmware` 开源键盘固件
- 组合键 Combo 激活回调 `process_combo_event`
- 找到 key_combos 结构体位置

### 输入分析
- 输入 `CHUNQIU` 激活 Combo_1
- 输入 `GAME` 激活 Combo_2
- 不同 Combo 激活不同 Layer

### Layer 结构
- 3 个 Layer，每个 Layer 有 108 个 keycode (6 列 × 18 行)
- Layer 2 中 0-9 位置继承上一层 keycode（KC_TRANSPARENT = 1）

### 还原脚本
```python
SEED = 0

def rand():
    global SEED
    SEED = 214013 * SEED + 2531011
    return (SEED >> 16) & 0x7fff

# keycodeToKey 字典 0-235 keycode 映射
keycodeToKey = {
    0: 'KC_NO', 1: 'KC_TRANSPARENT', 2: 'KC_POST_FAIL', 3: 'KC_UNDEFINED',
    4: 'KC_A', ..., 39: 'KC_0', 40: 'KC_ENTER', 41: 'KC_ESCAPE',
    42: 'KC_BACKSPACE', 43: 'KC_TAB', 44: 'KC_SPACE',
    ...
}

keymaps = [0x0029, 0x0000, 0x003A, 0x003B, ...]  # 3 层 × 108 个 keycode

# buildLayerMap 处理 KC_TRANSPARENT 继承
def buildLayerMap(layer):
    for i in range(108):
        curr_keycode = keymaps[layer * 108 + i]
        if curr_keycode == 1:  # KC_TRANSPARENT
            curr_keycode = keymaps[(layer - 1) * 108 + i]
        LayerMap[layer][keycodeToKey[curr_keycode]] = keycodeToKey[keymaps[i]]

formatLayer()
buildLayerMap(1)
buildLayerMap(2)
SEED = rand()
enc = "1CTED8IL-BIMM-SMFP-HOKP-HOIDRZL4W6KR"
Table = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
```

### 还原过程
1. 提取 `process_record_user` 函数
2. 根据当前 Layer 查 LayerMap 还原 keycode
3. LCG `SEED=0; SEED = 214013*SEED + 2531011; (SEED >> 16) & 0x7fff` 生成查表
4. 查 Table 还原明文 flag

## 经验提炼
- QMK 是开源键盘固件，组合键 (Combo) 触发 process_combo_event
- KC_TRANSPARENT (1) 继承上一层 keycode 是 QMK 关键特性
- LCG `SEED=0; rand = 214013*x + 2531011; (SEED >> 16) & 0x7fff` 是经典伪随机
- QMK 关键 keycode：`KC_A=4` `KC_Z=29` `KC_1=30` `KC_9=38` `KC_0=39`
- 6 列 × 18 行 = 108 位置是标准 QMK 键盘布局
- 找 process_combo_event 是 QMK 逆向起点
- keymaps 是 u16 数组存 keycode
