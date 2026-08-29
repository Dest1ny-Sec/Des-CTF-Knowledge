---
title: BCTF 自动驾驶 - WriteUp
contest: BCTF
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [ADC Autonomous Driving, Stanley controller, PID控制, Lane Detection targeted attack, KMeans聚类, deltaE_cie76, rgb2lab, GPS spoofing, npc_benign.json, latitude/longitude/altitude/yaw/speed, adversarial NPC, lane target attack]
attack_chain:
  - demo: Lane Detection targeted attack + ADC Programming interception
  - planning.py: Stanley controller (k_e=0.3, k_v=0.01) + delta_steer_per_iter=0.1
  - preprocess_image: 416x416 resize + BGR2RGB + transpose
  - waypoint_distance: np.sqrt(sum((waypt1-waypt2)**2))
  - normalize_angle: 限定 ±π
  - lateral_control: yaw_path + crosstrack_error + yaw_diff_crosstrack
  - longitudinal_control: PID(1.0, 0.1, 0.01, setpoint=5)
  - Adversarial NPC: 改 npc_benign.json 的 GPS 坐标, rate=1.2 缩放
  - pos[120+i].latitude = rate*(pos[120].latitude - pos[399].latitude) + pos[120+i].latitude
  - 写 gps_new.json 作为攻击 GPS
key_payload: 'Stanley controller k_e=0.3 k_v=0.01 / PID(1.0,0.1,0.01) / rate=1.2 GPS 缩放 / pos[120] vs pos[399] 锚点'
one_liner: BCTF 自动驾驶 — Stanley 横向控制 + PID 纵向控制 + Lane Detection targeted attack + Adversarial NPC GPS 缩放攻击 (rate=1.2 pos[120]/pos[399] 锚点)。
lesson: 自动驾驶对抗攻击: 横向 Stanley + 纵向 PID 控制;GPS 注入通过修改 npc JSON 即可;车道线检测可被 adversarial 干扰。
quality: high
---

# BCTF 自动驾驶 - WriteUp

## 速读
BCTF 自动驾驶赛题 — Lane Detection 目标攻击 + ADC Programming 拦截。

## 任务
1. **Lane Detection**: targeted attack
2. **ADC Programming**: interception

## planning.py 控制逻辑
```python
class Controller:
    def __init__(self):
        self.speed_pid = PID(1.0, 0.1, 0.01, setpoint=5)
        self.speed_pid.sample_time = 0.01
        self.speed_pid.output_limits = (-1, 1)
        self.last_steering = 0
        self.last_throttle = 0
        self.plan_waypts = []
    
    def get_control(self, adc_pose, adc_speed, adc_yaw, adc_frame, npc_poses):
        adc_frame_preprocessed = preprocess_image(adc_frame)
        # 横向 Stanley + 纵向 PID
        for i in range(len(npc_poses)):
            dist = waypoint_distance(adc_pose, npc_poses[i])
        if len(npc_poses) > 0:
            self.plan_waypts = [adc_pose, npc_poses[0]]
        steering = self.lateral_control(self.plan_waypts, adc_pose, adc_speed, adc_yaw, self.last_steering)
        throttle = self.longitudinal_control(adc_speed, dist)
        return steering, throttle
```

## 横向控制 Stanley
- `yaw_path = atan2(plan_waypts[-1].y - [0].y, [-1].x - [0].x)`
- `crosstrack_error = sqrt(min(sum((curr - plan)**2)))`
- `steer = normalize_angle(yaw_diff + atan(k_e * crosstrack / (k_v + v)))`

## 纵向控制 PID
- `self.speed_pid.setpoint = t_v` (目标速度)
- `throttle = self.speed_pid(v)`

## Adversarial NPC GPS 注入
```python
# 解析 npc_benign.json 拿 GPS 坐标
for line in gpslines:
    pos.append([la, lo, al, ti, ro, pi, ya, sp])

rate = 1.2
for i in range(len(pos) - 120):
    pos[120 + i].latitude = rate * (pos[120].latitude - pos[399].latitude) + pos[120 + i].latitude

# 写 gps_new.json
```
