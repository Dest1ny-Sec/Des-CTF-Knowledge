---
title: 2022 西湖论剑 IoT-AWD 赛题官方 WriteUp (下篇：三号固件)
contest: 2022 西湖论剑 IoT-AWD (下篇)
year: 2022
difficulty: hard
vuln_type: [pwn_unknown, auth_bypass, web_unknown, reverse, crypto_oracle]
tags: [IoT-AWD, OpenWrt, ubus, dsd, FIT-Image, uartlite, ns16550a, dts, IoT-安全, ubus_connect, D-Bus, hash-length-extension, ENV-var-bypass]
attack_chain: ["Q1 root shell: dumpimg 解包 itb, 看 dts, uartlite 状态 'disabled' → 改 'okay' → mkimage 重打包 → 串口 root", "uartlite 0x1e000c00 变 0x1e000d00, reg-shift 2, reg-io-width 4", "Q2 默认密码重置", "Q3 dsd: 逆向发现 ubus_connect, 走 OpenWrt ubus 协议", "Q4-Q10 各题: OpenWrt 漏洞 + 嵌入式 web + cgi-bin", "哈希长度扩展拿 token, ${PATH:offset:length} 绕大小写转换"]
key_payload: "uartlite status='okay' 后 mkimage 重新打包 itb 刷入"
one_liner: 西湖论剑 IoT-AWD 3 号固件：dts uartlite 启停 + ubus 协议 + OpenWrt
lesson: OpenWrt ubus 是 IoT 通用协议；dts 是嵌入式硬件配置
quality: high
---

# 2022 西湖论剑 IoT-AWD 赛题官方 WriteUp (下篇：三号固件)

原文 https://www.ctfiot.com/105793.html （海特实验室）

## 3 号固件

### Q1 root shell 获取 + 默认密码重置
**串口地址变化：**
- 一号固件：`0x1e000c00` (uartlite)
- 三号固件：`0x1e000d00` (uartlite2)

**dts 设备树：**
```dts
uartlite@c00 {
    compatible = "ns16550a";
    reg = <0xc00 0x100>;
    clock-frequency = <0x2faf080>;
    interrupt-parent = <0x01>;
    interrupts = <0x00 0x1a 0x04>;
    reg-shift = <0x02>;
    reg-io-width = <0x04>;
    no-loopback-test;
    status = "disabled";   // ← 关键
};
uartlite2@d00 {
    compatible = "ns16550a";
    reg = <0xd00 0x100>;
    status = "okay";        // ← 实际可用的
};
```

**修复：**
```bash
# dumpimg 解包 itb
# 改 status = "okay" 或删除 disabled 行
# mkimage 重新打包
# dfu-util 刷入
# 串口 → root
```

### Q2 默认密码重置
- 同第一题操作

### Q3 dsd (OpenWrt ubus)
```c
// 逆向 dsd 程序，发现 ubus_connect 函数
ubus_connect(ctx, "dsd", &dsd_obj);
```
- OpenWrt ubus 协议（类似 D-Bus）
- ubus 监听 unix socket `/var/run/ubus/ubus.sock`
- 通过 `ubus call dsd xxx` 调服务

### Q4-10
- CGI 后门 / 默认密码 / 已知 CVE
- 哈希长度扩展
- `${PATH:offset:length}` 绕大小写转换

## 教学价值
- **OpenWrt ubus** 是 IoT 通用协议
- **dts 设备树** 是嵌入式硬件配置
- **uartlite** 是 Xilinx 串口 IP
- **mkimage + dumpimg** (u-boot 工具) 是 FIT Image 必备
- **AWD 加固** = 关默认服务 / 改默认密码 / 删后门

## 工具
- dumpimg / mkimage
- dtc
- ubus CLI
- IDA Pro

## 关联
- 上篇 #83 1+2 号固件
- 2021 西湖论剑 IoT RW
- 海特实验室是国内 IoT 标杆
