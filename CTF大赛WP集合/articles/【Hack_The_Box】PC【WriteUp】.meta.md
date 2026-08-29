---
title: 【Hack The Box】PC【WriteUp】
contest: HackTheBox
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [rustscan, nmap, gRPC, grpcurl, evans, proto-reflection, SimpleApp, pyload, ssh-key, RCE, login-brute]
attack_chain: rustscan --top --ulimit 1500 扫 22/50051/grpc.reflection.v1alpha 服务 list 拿 SimpleApp/evans 或 grpcurl 调 LoginUser 用户名密码（遍历）/get user id 后 pyload 上传文件走 SSH 公私钥登录 get shell
key_payload: 端口 22 + 50051 (gRPC)  SimpleApp.LoginUser  Python gRPC client
one_liner: Hack The Box PC 题，gRPC 50051 端口反射枚举 + LoginUser 用户枚举 + pyload SSH 登录。
lesson: rustscan 比 nmap 快的现代端口扫描器；gRPC 服务默认在 50051 端口，需用 grpcurl/evans 工具；grpc.reflection.v1alpha 反射服务可枚举所有方法和消息。
quality: high
---

# 【Hack The Box】PC【WriteUp】

## 概览
HackTheBox PC 题目 WP，gRPC 50051 端口反射枚举 + 凭据爆破 + SSH 登录。

## 端口扫描
```bash
rustscan -a 10.129.95.145 --top --ulimit 1500
# Open 10.129.95.145:22 (SSH)
# Open 10.129.95.145:50051 (gRPC)
```

## gRPC 服务枚举
```bash
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
go install github.com/ktr0731/evans@latest

/root/go/bin/grpcurl -plaintext 10.129.95.145:50051 list
# SimpleApp
# grpc.reflection.v1alpha.ServerReflection
```

## 攻击链

### Stage 1: gRPC 方法枚举
- `grpcurl -plaintext 10.129.95.145:50051 list SimpleApp` 列出方法
- `grpcurl -plaintext 10.129.95.145:50051 describe SimpleApp.LoginUser` 描述消息
- 用 evans 交互：`evans -p 50051 -h 10.129.95.145`

### Stage 2: LoginUser 用户枚举
- 遍历常见用户名 admin/root/test/sau 等
- 寻找响应中泄露的 user_id 或 token

### Stage 3: pyload + SSH 登录
- 上传 SSH 公钥到目标用户家目录
- 用 gRPC 调用 PutFile / UploadFile 方法
- 用私钥 SSH 登录 get shell

## 经验提炼
- rustscan 比 nmap 快的现代端口扫描器（基于 Rust + Tokio）
- gRPC 服务默认在 50051 端口，需用 grpcurl/evans 工具
- grpc.reflection.v1alpha.ServerReflection 反射服务可枚举所有方法和消息
- pyload 工具可从 gRPC 响应解析 proto 文件
- 用户枚举走 LoginUser 这种"登录"接口是常见入口
- 上传 SSH 公钥到 home 是经典提权方式

## 工具链
- **rustscan**: 端口扫描（`--top` 扫 TOP 100，`--ulimit 1500` 提升文件描述符）
- **nmap**: 详细服务识别
- **grpcurl**: gRPC 客户端（类似 curl）
- **evans**: gRPC 交互式 REPL
- **pyload**: Python gRPC 客户端生成
