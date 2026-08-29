---
title: 第九届"强网杯"行业领域专项赛车联网安全赛-复赛（零部件测试）WP
contest: 第九届强网杯车联网安全赛复赛
year: 2025
difficulty: easy
vuln_type: misc_unknown
tags: [强网车联网复赛, ADB, data/local/tmp, 签到+APP+固件, jadx, 010 Editor搜flag, 远程车机环境吐槽]
attack_chain: ADB连接远程车机→/data/local/tmp目录→签到读password.txt→APP题jadx看主函数→固件题010 Editor搜flag→OTA题分析流量包
key_payload: "/data/local/tmp;password.txt;jadx;010 Editor搜flag;ADB"
one_liner: 第九届强网车联网复赛（零部件测试）4题：password.txt签到+APP+固件+OTA流量分析
lesson: 车机环境基本是/data/local/tmp下的CTF题；远程车机环境易崩
quality: low
---

# 第九届"强网杯"行业领域专项赛车联网安全赛-复赛（零部件测试）WP

**赛事**：第九届强网杯车联网安全赛复赛（2025）

**吐槽**：远程车机环境不稳定，504 Gateway Time-out，工具上传报错，无后续解决

**4道题解**：

**1. 强网复赛-签到**：
- `/data/local/tmp` 下有 `password.txt`
- 读取即可

**2. 强网复赛-APP**：
- `/data/local/tmp` 下有 `app`
- jadx打开找主函数 → flag

**3. 强网复赛-固件**：
- `/data/local/tmp` 下有固件包
- adb pull 拉取
- 010 Editor 搜索 flag

**4. 强网复赛-OTA**（未完成）：
- `/data/local/tmp` 下有流量包
- 应分析流量包提取下载的固件
- 在固件中找flag

**质量评估**：低（基础题+环境吐槽）
