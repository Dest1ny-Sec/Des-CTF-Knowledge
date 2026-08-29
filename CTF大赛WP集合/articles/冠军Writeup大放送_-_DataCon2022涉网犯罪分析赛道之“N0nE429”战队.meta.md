---
title: 冠军Writeup大放送 | DataCon2022涉网犯罪分析赛道之"N0nE429"战队
contest: DataCon2022 涉网犯罪分析
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [DataCon, 攻击者画像, 同源关联, 风险评级, Mirai样本, IOC提取, signal函数, resolve_cnc_addr, table加密, MongoDB]
attack_chain:
  - 武汉大学 N0nE429 战队 (JackNoire/Jiryu/Scorpion) 师从傅建明
  - 攻击者画像 6 类: 安全公司/非恶意互联网应用/僵尸网络/白帽黑客/雇佣黑客/未知
  - 风险评级 6 档: 基本可信/低风险/中风险/中高风险/高风险/特殊
  - 数据源: attack-log (WAF web 告警) + frame-tag (IP属性/DNS/hack-tool)
  - MongoDB 存储 (记录长度受限, 略大文件单独处理)
  - 冬奥 2.4-2.20 期间 602 个 IP 切片
  - 指标: is_dangerous/is_proxy/is_gateway/is_tor/is_gov_targeted/has_webshell/has_hacktool
  - 同源: 相同风险+相同身份+IP 主机号接近
  - Mirai IOC: idapython 定位 main → signal(SIGTRAP=5, &anti_gdb_entry)
  - resolve_cnc_addr 三种形式: 直接赋值/字符串传参/table 加密
  - table 加密: TABLE_CNC_DOMAIN/TABLE_CNC_PORT → table_retrieve_val
  - 加密函数: 统计 logic 7-9 + airthmetic 2-4 指令
key_payload: '攻击者画像 6 类+评级 6 档 + Mirai IOC 自动化提取 (idapython)'
one_liner: DataCon2022 涉网犯罪分析冠军 N0nE429：WAF 日志+frame-tag 攻击者画像+同源关联 + Mirai IOC 自动化提取。
lesson: 攻击者画像核心是建立指标体系 (is_dangerous/is_proxy/is_gov_targeted 等)；Mirai 反编译定位 main→signal(SIGTRAP)→anti_gdb_entry→resolve_cnc_addr→table 加密是自动化 IOC 提取关键链。
quality: high
---

# 冠军Writeup大放送 | DataCon2022涉网犯罪分析赛道之"N0nE429"战队

## 概览
- **来源**: ctfiot 91525
- **赛事**: DataCon2022 涉网犯罪分析赛道冠军
- **战队**: 武汉大学 N0nE429 (JackNoire/Jiryu/Scorpion 傅建明教授)
- **难度**: ⭐⭐⭐⭐

## 攻击者画像 6 类

| 类型 | 特征 |
|------|------|
| 安全公司 | 明确基础设施 (低/中能力) |
| 非恶意互联网应用 | 资产测绘/爬虫, 误报 |
| 僵尸网络 | 批量化挖矿/控制, 自动化特征 |
| 白帽黑客 | 安全爱好者, 历史攻击事件 |
| 雇佣黑客 | 高能力/针对性/政治目的 (APT) |
| 未知属性 | 数据视野无法确认 |

## 风险评级 6 档

| 评级 | 说明 |
|------|------|
| 基本可信 | 授权检测/爬虫 |
| 低风险威胁 | 脚本小子/老旧漏洞僵尸网络 |
| 中风险威胁 | webshell/规模化攻击 |
| 中高风险威胁 | 雇佣黑客/APT, 有针对性 |
| 高风险威胁 | APT 强针对性 |
| 特殊 | 无云端情报, 需二次分析 |

## 数据源
- **attack-log**: WAF web 告警 (IP+日期 切片)
- **frame-tag**:
  - domain-info-host: IP 绑定域名
  - ip-info: IP 属性
  - payload-domain-parser: 攻击载荷域名
  - attack-timeline: 攻击摘要
  - hack-tool: 攻击者工具
  - special-behavior: DNS 命中规则

## 指标体系
- is_dangerous / is_proxy / is_gateway / is_tor
- is_gov_targeted (针对 .gov.cn)
- has_webshell / has_hacktool / has_scanner
- has_vuln_xx (特定漏洞)

## Mirai IOC 自动化提取
```python
# 1. 定位 main (ARM: LDR R0,=main / X86: push offset main)
# 2. 找 signal(SIGTRAP=5, &anti_gdb_entry) 
# 3. anti_gdb_entry → resolve_cnc_addr
# 4. resolve_cnc_addr 三种形式:
#    - 直接赋值: sock_addr.sin_port + sin_addr
#    - 字符串传参: 正则判断 IP/域名
#    - table 加密: TABLE_CNC_DOMAIN + TABLE_CNC_PORT
# 5. 加密函数识别: logic 7-9 + airthmetic 2-4 指令
# 6. 提取 table 地址 + table_key
```

## 教学
- 攻击者画像 = 指标 + 规则 + 同源
- Mirai 反编译核心: signal → anti_gdb → resolve_cnc_addr → table
- 自动化 IOC 提取要支持 ARM/X86 双架构
