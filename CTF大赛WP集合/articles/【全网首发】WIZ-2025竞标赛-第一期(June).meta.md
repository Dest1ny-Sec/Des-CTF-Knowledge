---
title: 【全网首发】WIZ-2025 竞标赛 第一期(June) Perimeter Leak
contest: WIZ
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [WIZ-CTF, cloud-security, AWS-S3, Spring-Boot-Actuator, IMDSv1, IMDSv2, data-perimeter, cloud-CTF]
attack_chain: 1. Spring Boot Actuator /actuator/env /actuator/heapdump 暴露敏感信息/2. IMDSv1 169.254.169.254/latest/meta-data/ 直接访问/3. AWS S3 存储桶 flag 提取/4. data perimeter 限制 + 凭证提权
key_payload: /actuator/heapdump  IMDSv1 169.254.169.254  AWS S3
one_liner: WIZ-2025 竞标赛第一期 Perimeter Leak，Spring Boot Actuator + IMDS 攻击 + AWS S3 数据外泄。
lesson: Spring Boot Actuator 暴露 heapdump 含密钥；IMDSv1 无认证可访问，IMDSv2 需 token；AWS data perimeter 是 S3 访问控制机制；cloud CTF 三大攻击面。
quality: high
---

# 【全网首发】WIZ-2025 竞标赛 第一期(June) Perimeter Leak

## 概览
WIZ 2025 6 月开始的云 CTF 锦标赛，主题 Perimeter Leak（周边泄漏），由 miao2sec 团队 CDxiaodong 完成 WP。

## 关键点
- "S3 存储桶中提取出隐藏的 flag"：flag 存储在 S3 中
- "使用了 AWS 数据边界（data perimeter）来限制对该存储桶内容的访问"：需凭证提权
- "部署在 AWS 上的 Spring Boot Actuator 应用"：Spring Boot Actuator 配置不当暴露敏感信息

## 攻击链

### Stage 1: Spring Boot Actuator 攻击
- `/actuator/env` 暴露环境变量
- `/actuator/heapdump` 下载堆转储（包含密钥）
- `/actuator/beans` 列所有 Bean

### Stage 2: IMDS 攻击
**IMDSv1**:
```
http://169.254.169.254/latest/meta-data/
```
- 直接访问，无需 token

**IMDSv2**:
- 需 PUT 请求获取 token
- 带回 token 头访问元数据

### Stage 3: S3 数据外泄
- 获得 IAM 凭证后访问 S3
- data perimeter 是 AWS 访问控制
- 越权访问 S3 获取 flag

## IMDS 关键路径
| 路径 | 内容 | 攻击价值 |
|------|------|----------|
| instance-id | 实例 ID | 信息性 |
| ami-id | 当前 AMI | 信息性 |
| iam/security-credentials/ | IAM 角色临时凭证 | **高价值** |
| network/interfaces/ | 网络信息 | 信息性 |
| public-keys/ | 公钥 | 中价值 |

## 经验提炼
- Spring Boot Actuator 暴露 heapdump 含密钥
- IMDSv1 无认证可访问，IMDSv2 需 token
- AWS data perimeter 是 S3 访问控制机制
- cloud CTF 三大攻击面：actuator/IMDS/S3
- PUT 请求获取 IMDSv2 token
- 169.254.169.254 是云元数据 IP
- heapdump 包含明文密码/JWT 密钥
- AWS 凭证 1 小时过期
- Spring Boot 1.x 默认无 actuator，2.x 部分默认
- WIZ 是 Wiz Research，云安全明星机构
