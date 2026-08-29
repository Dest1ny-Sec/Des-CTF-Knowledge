---
title: 记一次用 AI 打比赛
contest: BlockHarbor 比赛
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [AI-assisted, CAN-bus, UDS, caringcaribou, automotive-security, RDBI-dump, security-access, seed-answer, firmware-signing, rockyou]
attack_chain:
- 题目1AutoGraph: RAMN ECU B和C的caringcaribou UDS RDBI dump日志+签名固件,提示flag是十进制secret key
- 用rockyou.txt爆破压缩包密码(字母+数字爆不出来)
- 从candump日志重建完整固件+识别Security Access算法
- ECU C给出seed 9A5ABF0C1CAAFDEB72761E909501D6E9,求answer(32位hex大写)
- 题目2ECU C: SecurityAccess算法逆向,seed→key计算
- flag是十进制格式的secret key
key_payload: 32位hex大写answer
one_liner: BlockHarbor汽车安全比赛AI辅助WP,涵盖caringcaribou UDS RDBI dump+Security Access算法逆向+CAN日志固件重建+seed→key计算,rockyou.txt爆破压缩包密码。
lesson: 汽车安全比赛常考UDS(统一诊断服务)+CAN总线+caringcaribou工具;SecurityAccess算法(Seed→Key)需要逆向固件提取;rockyou.txt是国外比赛压缩包密码首选字典。
quality: medium
---

## 题目列表

BlockHarbor比赛,2道红队题:
1. AutoGraph [RAMN] (CAN dump+固件签名)
2. ECU C Security Access算法逆向

## 关键考点

### 工具链
- caringcaribou:Python UDS/CAN工具,支持RDBI(ReadDataByIdentifier)dump
- candump:SocketCAN工具,记录(时间戳) (can接口) (CANID)#(CAN数据)
- rockyou.txt:国外比赛压缩包密码爆破首选字典

### 题目1: AutoGraph [RAMN]
- 附件:candump日志+带密码压缩包(签名固件)
- 提示:flag是十进制格式的secret key,不是压缩包密码
- 步骤:
  1. 用rockyou.txt爆破压缩包密码
  2. 从candump日志重建固件映像
  3. 识别Security Access算法(常见汽车安全算法)
  4. 提取secret key(十进制)

### 题目2: ECU C Security Access
- 提示:ECU C的Security Access算法已更新,无法解锁
- 给出seed:9A5ABF0C1CAAFDEB72761E909501D6E9
- 求answer:32位hex大写字符串
- 步骤:
  1. 提取固件中Security Access算法实现
  2. 逆向seed→key计算逻辑
  3. 输入seed计算answer

### 通用UDS安全访问流程
1. Tester发送27 01(SecurityAccess RequestSeed)
2. ECU返回seed
3. Tester用算法计算key
4. Tester发送27 02(SecurityAccess SendKey)+key
5. ECU验证key正确性,返回67 02(PositiveResponse)

## 实战价值
- 汽车安全(ISO 21434)+ UDS(ISO 14229)是新兴CTF方向
- caringcaribou是入门必备工具
- SecurityAccess算法(Seed→Key)是UDS核心安全机制
- rockyou.txt是国外比赛通用密码字典
