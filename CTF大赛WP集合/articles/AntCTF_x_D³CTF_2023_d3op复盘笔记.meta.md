---
title: AntCTF x D³CTF 2023 d3op 复盘笔记
contest: D³CTF
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [OpenWrt 22.03.3, gambox, squashfs-root, diff rootfs, base64 ubus module, /etc/shadow $6$JlPmKq, unauthenticated.json, network.interface, vuln_point, init_base64, check_method]
attack_chain:
  - 解 gambox 固件 → OpenWrt 22.03.3 r20028-43d71ad93e squashfs-root
  - 从官网下载同版本 OpenWrt 22.03.3 diff
  - diff 关键: /etc/shadow root $6$JlPmKq/ZhqQ0I6V6$ 哈希密码
  - 多了 /flag 文件
  - 多了 /usr/libexec/rpcd/base64 (ubus 模块)
  - unauthenticated.json 加 base64 encode/decode 允许未授权
  - 多了 /etc/config/network
  - 漏洞点: base64 模块 + network.interface 配置
  - 启动后 init_base64() + main 接受 list/encode/decode 命令
  - read_input(0, v6, 0xFFF) 读 stdin
  - sub_402478 解析 + sub_403C90 找 "input" 字段 + sub_4059D0 验证
key_payload: 'diff rootfs / base64 ubus / unauthenticated.json / $6$ shadow / /flag / network.interface / init_base64 + check_method'
one_liner: AntCTF x D³CTF 2023 d3op — OpenWrt 22.03.3 固件 diff 找 base64 ubus 模块 + /etc/shadow 哈希 + /flag + network.interface 攻击面。
lesson: OpenWrt 固件题标准做法:官网下同版本 diff;base64 是 ubus 微系统总线模块;$6$ 是 sha512 crypt;unauthenticated.json 控制 ACL。
quality: high
---

# AntCTF x D³CTF 2023 d3op 复盘笔记

## 速读
D³CTF 2023 + AntCTF 联合赛 — OpenWrt 22.03.3 路由器固件题。

## 固件分析
```
OpenWrt 22.03.3, r20028-43d71ad93e
```

## diff 关键差异
| 路径 | 差异 |
|------|------|
| /etc/shadow | root $6$JlPmKq/ZhqQ0I6V6$ 哈希密码 |
| /flag | 新增 flag 文件 |
| /usr/libexec/rpcd/base64 | 新增 ubus base64 模块 |
| /etc/config/network | 新增 network 配置 |
| /usr/share/rpcd/acl.d/unauthenticated.json | 加 base64.encode/decode |

## unauthenticated.json 改动
```json
{
  "unauthenticated": {
    "description": "Access controls for unauthenticated requests",
    "read": {
      "ubus": {
        "session": ["access", "login"],
        "base64": ["decode", "encode"]
      }
    }
  }
}
```

## ubus 调用
```bash
ubus list
# base64, network, file, session, system, uci 等

ubus call base64 encode '{"input" : "z1r0"}'
# {"output": "ejFyMAA="}
```

## main 二进制
```c
int main(int argc, char **argv, char **envp) {
    char v6[4096];
    init_base64();
    if (argc <= 1) return 0;
    method = argv[1];
    if (check_method(method, "list")) {
        v10 = read_input(0, v6, 0xFFFuLL);
        v6[v10] = 0;
        v9 = sub_402478(v6);     // 解析 JSON
        v8 = sub_403C90(v9, "input");
        ...
    }
}
```
