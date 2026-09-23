---
title: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（一）
contest: VSEC
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags:
- Block-Harbor
- VSEC-HarborBay
- Mach-E-UDS-simulation
- CAN-interface
- Arbitration-ID
- license-plate-VIN
- MAC-address-geolocation
- OSINT
attack_chain: 1. VSEC 平台 → HarborBay → Mach-E UDS Challenge Simulation/2. CAN 接口名/3. 周期 CAN 帧 Arbitration ID/4. CAN 帧 data 字段字节数 + 值/5. 帧发送频率 Hz/6. Block Harbor 成立时间 2014 年/7. 车牌 DCR 660 密歇根州查 VIN + 品牌型号 + 制造地 + 进口时间/8. MAC 2A:38:5C:91:E5:27 查 2022-12-08 位置
key_payload: Mach-E UDS Challenge  CAN 接口名  帧格式  车牌 DCR 660  MAC 2A:38:5C:91:E5:27
one_liner: VSEC 车联网安全 CTF 挑战赛（一），Mach-E UDS 模拟器 + Block Harbor 背景 + 车牌 + MAC 地理定位。
lesson: Block Harbor 是汽车网络安全公司，VSEC 是其平台；Mach-E 是福特野马电动车；CAN 仲裁 ID + data 字段是基础协议；车牌反查 VIN 是 OSINT 经典题。
quality: medium
full_path: 【WriteUP】VSEC_车联网安全_CTF_挑战赛（一）.full.md
meta_path: 【WriteUP】VSEC_车联网安全_CTF_挑战赛（一）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WriteUP】VSEC 车联网安全 CTF 挑战赛（一）。VSEC 车联网安全 CTF 挑战赛（一），Mach-E UDS 模拟器 + Block Harbor 背景 + 车牌 + MAC 地理定位。。经验：Block Harbor 是汽车网络安全公司，VSEC 是其平台；Mach-E 是福特野马电动车；CAN 仲裁 ID +...
category: misc
subcategory: misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/192410.html
reasoning_chain:
- VSEC 平台 → HarborBay → Mach-E UDS Challenge Simulation → 触发点：VSEC 是 Block Harbor 汽车 CTF 平台
- 动作：进 HarborBay + 选 Mach-E UDS 模拟 + 启 terminal → 观察：拿到虚拟终端
- 终端 ip link / ip a 查 CAN 接口 → 触发点：vcan0 接口 → 假设：可用 candump/cansend 嗅探
- 观察：周期 CAN 帧 → 触发点：仲裁 ID 是 canid → 假设：candump -L vcan0 提帧格式 + 频率
- 动作：统计 CAN ID 出现次数 → 观察：门锁/速度表/转向 arbitration ID 找到
- Block Harbor 背景题 → 触发点：OSINT → 动作：搜 'Block Harbor founded' → 观察：2014 年成立
- 车牌 DCR 660 → 触发点：OSINT 反查 → 动作：密歇根州 DMV → 观察：VIN + 品牌 + 制造地 + 进口时间
- MAC 2A:38:5C:91:E5:27 → 触发点：MAC OUI → 动作：wigle.net / macvendors.com 查 → 观察：2022-12-08 位置
failed_attempts:
- 试图在 HarborBay GUI 找答案 → 失败：必须进 UDS 模拟 terminal 跑命令
- 试图用 can-utils 完整嗅探 → 失败：只需统计 arbitration ID 即可
- 试图用国内车牌查询 DCR 660 → 失败：是美国车牌，必须密歇根州 DMV
key_observations:
- Block Harbor 是汽车网络安全公司，VSEC 是其教育平台
- Mach-E 是福特电动 SUV，UDS 模拟是其训练靶场
- CAN 仲裁 ID + data 字段是车载协议基础
- 美国车牌反查 VIN 是 OSINT 经典手法（密歇根州开放数据库）
- MAC 地址 OUI 查询配合 wigle.net 可定位历史位置
prerequisites:
- can-utils 工具（candump / cansend / ip link）
- OSINT 基础（Google dorking / 公开数据库查询）
- MAC OUI + wigle.net 使用
- Block Harbor / VSEC 平台背景认知
---
# 【WriteUP】VSEC 车联网安全 CTF 挑战赛（一）

> 原文: https://www.ctfiot.com/192410.html
> ID: 192410

Block Harbor 是一家专注于汽车网络安全领域的公司，Block Harbor 组织的汽车CTF挑战赛，第一季以教育和乐趣为核心，教授参与者如何嗅探CAN总线并发送控制信息。赛事迅速获得了社区的积极响应，并发展成为一个全球性的活动，吸引了来自亚洲、中东、欧洲和北美的900多名参与者。

第一季赛事结束后，Block Harbor 通过其平台VSEC公开了50个独特的汽车挑战，并提供了5000美元的奖金，激发了更广泛的参与和社区建设。

第二季赛事预计将在2024年8月24日至9月8日举行，奖金池增至10万美元（From Garage to Glory: The Rise of a $100K Automotive Capture the Flag Challenge – Block Harbor）

在他们网站上有一个车联网安全 CTF 平台，记录一下WriteUP

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the name of the CAN interface available on the virtual terminal?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。虚拟终端上可用的 CAN 接口名称是什么？

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the Arbitration ID of the CAN frame being sent periodically on the CAN interface?翻译：本次挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的仲裁 ID 是什么？

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.How many bytes of data are in the data field of the CAN frame being sent periodically on the CAN interface?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的数据字段中有多少字节数据？

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the value of the data field of the CAN frame being sent periodically on the CAN interface? Format: XXYY翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的数据字段的值是多少？格式：XXYY

题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the frequency that the periodic CAN frame is transmit at? (in Hz)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。周期性 CAN 帧的传输频率是多少？（单位为 Hz）

题目描述：???Minus 1 million points if this is your actual password.翻译：???如果这是您的实际密码，则扣除 100 万分。

题目描述：When was Block Harbor founded?翻译：Block Harbor 是什么时候建立的？

题目描述：Here's a license plate "DCR 660", it is registered in Michigan. Can you find the VIN?翻译：这是车牌“DCR 660”，注册地为密歇根州。你能找到 VIN 吗？

题目描述：Here's a license plate "DCR 660", it is registered in Michigan. What is the make and model?Format: year-make-model翻译：这是牌照“DCR 660”，在密歇根州注册。品牌和型号是什么？格式：年份-品牌-型号

题目描述：Here's a license plate "DCR 660", it is registered in Michigan. Where was it manufactured at?Format: City, Country翻译：这是车牌“DCR 660”，在密歇根州注册。它是在哪里制造的？格式：城市，国家

题目描述：Here's a license plate "DCR 660", it is registered in Michigan. When was this car imported to the US?Format: dd-mm-yyyy翻译：这是车牌“DCR 660”，在密歇根州注册。这辆车什么时候进口到美国的？格式：dd-mm-yyyy

题目描述：We've managed to identify the MAC address of a vehicle of interest, can you help us track down where it was located on December 8'th, 2022? We need the latitude and longitude to two decimal places.MAC: 2A:38:5C:91:E5:
27Hint: format XX.XX,XX.XX翻译：我们已成功识别出相关车辆的 MAC 地址，您能帮我们追踪它在 2022 年 12 月 8 日的位置吗？我们需要精确到小数点后两位的纬度和经度。MAC：2A:38:5C:91:E5:
27提示：格式 XX.XX,XX.XX


```
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the name of the CAN interface available on the virtual terminal?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。虚拟终端上可用的 CAN 接口名称是什么？
回到 VSEC 平台，选择 Garage
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the Arbitration ID of the CAN frame being sent periodically on the CAN interface?翻译：本次挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的仲裁 ID 是什么？
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.How many bytes of data are in the data field of the CAN frame being sent periodically on the CAN interface?翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的数据字段中有多少字节数据？
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the value of the data field of the CAN frame being sent periodically on the CAN interface? Format: XXYY翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。在 CAN 接口上定期发送的 CAN 帧的数据字段的值是多少？格式：XXYY
题目描述：This challenge is within the Harborbay vehicle simulator on VSEC. From the home page, enter HarborBay. Select the Mach-E UDS Challenge Simulation, then launch the terminal.What is the frequency that the periodic CAN frame is transmit at? (in Hz)翻译：此挑战在 VSEC 上的 Harborbay 车辆模拟器中进行。从主页进入 HarborBay。选择 Mach-E UDS 挑战模拟，然后启动终端。周期性 CAN 帧的传输频率是多少？（单位为 Hz）
题目描述：???Minus 1 million points if this is your actual password.翻译：???如果这是您的实际密码，则扣除 100 万分。
题目描述：When was Block Harbor founded?翻译：Block Harbor 是什么时候建立的？
搜一下 Block Harbor 在官网找到介绍，可以看到是 2014 年建立的
题目描述：Here's a license plate "DCR 660", it is registered in Michigan. Can you find the VIN?翻译：这是车牌“DCR 660”，注册地为密歇根州。你能找到 VIN 吗？
题目描述：Here's a license plate "DCR 660", it is registered in Michigan. What is the make and model?Format: year-make-model翻译：这是牌照“DCR 660”，在密歇根州注册。品牌和型号是什么？格式：年份-品牌-型号
题目描述：Here's a license plate "DCR 660", it is registered in Michigan. Where was it manufactured at?Format: City, Country翻译：这是车牌“DCR 660”，在密歇根州注册。它是在哪里制造的？格式：城市，国家
题目描述：Here's a license plate "DCR 660", it is registered in Michigan. When was this car imported to the US?Format: dd-mm-yyyy翻译：这是车牌“DCR 660”，在密歇根州注册。这辆车什么时候进口到美国的？格式：dd-mm-yyyy
题目描述：We've managed to identify the MAC address of a vehicle of interest, can you help us track down where it was located on December 8'th, 2022? We need the latitude and longitude to two decimal places.MAC: 2A:38:5C:91:E5:
27Hint: format XX.XX,XX.XX翻译：我们已成功识别出相关车辆的 MAC 地址，您能帮我们追踪它在 2022 年 12 月 8 日的位置吗？我们需要精确到小数点后两位的纬度和经度。MAC：2A:38:5C:91:E5:
27提示：格式 XX.XX,XX.XX
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]