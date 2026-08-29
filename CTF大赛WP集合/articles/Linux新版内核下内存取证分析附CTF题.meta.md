---
title: Linux 新版内核下内存取证分析附 CTF 题
contest: 取证
year: 2022
difficulty: hard
vuln_type: forensic_memory
tags: [Volatility2, dwarf2json, Ubuntu 22.04, Linux 5.15, bip39 mnemonic]
attack_chain: |
  1. 背景: Volatility2 在 Ubuntu 22.04 尚未实现，5.15.0-43-generic 内存镜像需要 profile
  2. 方案 A: docker 跑 volatility2/tools/linux
     - docker run -it --rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
     - apt install linux-headers-5.15.0-43-generic linux-image-5.15.0-43-generic dwarfdump build-essential
     - sed -i 's/$(shell uname -r)/5.15.0-43-generic/g' Makefile
     - echo 'MODULE_LICENSE("GPL");' >> module.c
     - make
     - zip Linux-5.15.0-43-generic.zip module.dwarf /boot/System.map-5.15.0-43-generic
  3. 方案 B: dwarf2json 工具 (Volatility3 推荐)
     - git clone https://github.com/volatilityfoundation/dwarf2json
     - cd dwarf2json && go build
     - wget linux-image-unsigned-5.15.0-48-generic-dbgsym_*.ddeb
     - dpkg -i *.ddeb
     - ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.15.0-48-generic > linux-image-5.15.0-48-generic.json
  4. 拷贝 JSON profile 到 volatility3/volatility3/framework/symbols/linux/
  5. Volatility3 插件: banners/bash/check_afinfo/check_creds/check_idt/check_modules/check_syscall/elfs/keyboard_notifiers/kmsg/lsmod/lsof/malfind/mountinfo/proc/psaux/pslist/pstree/tty_check
  6. CTF 题: dump.mem 镜像 → vol.py -f dump.mem linux.psaux.PsAux
  7. bip39 mnemonic 解密: code = 0x26F4036773F33FD1BC4E55616472CD7F65086B670B2DD5B84BB4D16F02730E734F72E500
     - bin(code) → 12-bit 分段查 bip39 词典
     - 11 words mnemonic → bip39 钱包恢复
key_payload: |
  # Volatility2 profile 生成 (docker):
  docker run -it --rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
  apt install -y linux-headers-5.15.0-43-generic linux-image-5.15.0-43-generic dwarfdump build-essential
  cd /volatility/tools/linux
  sed -i 's/$(shell uname -r)/5.15.0-43-generic/g' Makefile
  echo 'MODULE_LICENSE("GPL");' >> module.c
  make
  zip Linux-5.15.0-43-generic.zip module.dwarf /boot/System.map-5.15.0-43-generic
  
  # Volatility3 profile 生成 (dwarf2json):
  git clone https://github.com/volatilityfoundation/dwarf2json && cd dwarf2json && go build
  wget https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb
  dpkg -i linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb
  ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.15.0-48-generic > linux-image-5.15.0-48-generic.json
  cp linux-image-*.json volatility3/volatility3/framework/symbols/linux/
  
  # Volatility3 启动:
  python vol.py -f dump.mem linux.psaux.PsAux
  python vol.py -f dump.mem linux.pslist.PsList
  python vol.py -f dump.mem linux.bash.Bash
  python vol.py -f dump.mem linux.malfind.Malfind
  
  # bip39 mnemonic 解密:
  code = 0x26F4036773F33FD1BC4E55616472CD7F65086B670B2DD5B84BB4D16F02730E734F72E500
  code = bin(code)[2:].zfill((len(code) + (12 - len(code) % 12)))
  mnemonic = [words[int(code[i:(i+12)], 2) - 1] for i in range(0, len(code), 12)]
  print(" ".join(mnemonic))
one_liner: Linux 5.15 新版内核的 Volatility2/3 profile 生成方法 (docker + dwarf2json) + bip39 钱包 mnemonic 解密 CTF 题。
lesson: |
  - Volatility2 在 Ubuntu 22.04 跑不动，需要 docker + ubuntu 20.04 + 对应 kernel headers
  - Volatility3 推荐 dwarf2json 工具: 直接读 vmlinux debug 符号生成 ISF JSON profile
  - profile 是 ZIP 包 (vol2) 或 JSON 文件 (vol3) 必须放到 plugins/overlays/linux 目录
  - volatility3 插件: linux.psaux / pslist / bash / malfind / mountinfo / proc / lsof
  - bip39 mnemonic: 12-bit 分段查 2048 词表 → 12/24 words 恢复钱包
  - 内存取证 CTF 题常用: bash history / proc maps / malfind (RWX 区域) / 文件恢复
quality: high
---

# Linux 新版内核下内存取证分析附 CTF 题

> 来源: ctfiot.com 60876

## 背景

- Volatility2 在 Ubuntu 22.04 尚未成功实现
- 5.15.0-43-generic 内存镜像需要 profile
- 提供两种方案：docker 跑旧版 + dwarf2json 跑新版

## 方案 A: docker + Volatility2

```bash
docker run -it --rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
apt install -y linux-headers-5.15.0-43-generic \
    linux-image-5.15.0-43-generic dwarfdump build-essential
cd /volatility/tools/linux
sed -i 's/$(shell uname -r)/5.15.0-43-generic/g' Makefile
echo 'MODULE_LICENSE("GPL");' >> module.c
make
zip Linux-5.15.0-43-generic.zip \
    module.dwarf /boot/System.map-5.15.0-43-generic
```

把生成的 zip 拷贝到 `volatility2/volatility/plugins/overlays/linux/`，Volatility2 自动识别。

## 方案 B: dwarf2json (Volatility3 推荐)

```bash
git clone https://github.com/volatilityfoundation/dwarf2json
cd dwarf2json && go build

# 下载 ubuntu dbgsym
wget https://launchpad.net/ubuntu/+archive/primary/+files/\
    linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb
dpkg -i linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb

./dwarf2json linux \
    --elf /usr/lib/debug/boot/vmlinux-5.15.0-48-generic \
    > linux-image-5.15.0-48-generic.json

cp linux-image-*.json \
    volatility3/volatility3/framework/symbols/linux/
```

## Volatility3 插件

```
banners.Banners / bash.Bash / check_afinfo.Check_afinfo /
check_creds.Check_creds / check_idt.Check_idt /
check_modules.Check_modules / check_syscall.Check_syscall /
elfs.Elfs / keyboard_notifiers.Keyboard_notifiers /
kmsg.Kmsg / lsmod.Lsmod / lsof.Lsof / malfind.Malfind /
mountinfo.MountInfo / proc.Maps / psaux.PsAux / pslist.PsList /
pstree.PsTree / tty_check.tty_check
```

```bash
python vol.py -f dump.mem linux.psaux.PsAux
python vol.py -f dump.mem linux.bash.Bash
python vol.py -f dump.mem linux.malfind.Malfind
```

## CTF 题: bip39 Mnemonic 解密

```python
import sys
try:
    password = sys.argv[1]
except:
    print("Usage: ./wallet password")
    exit()

words = []
with open("bip39list.txt", "r") as f:
    words = f.read().splitlines()

code = 0x26F4036773F33FD1BC4E55616472CD7F65086B670B2DD5B84BB4D16F02730E734F72E500
code = bin(code)[2:]
code = str(code.zfill((len(code) + (12 - len(code) % 12))))

mnemonic = []
for i in range(0, len(code), 12):
    mnemonic.append(words[int(code[i:(i+12)], 2) - 1])
print(" ".join(mnemonic))
```

把 hex → bin → 12-bit 分段 → 查 bip39 词表 → 输出 11 个助记词 → 钱包恢复。

## 评价

Linux 5.15 新版内核内存取证的工程性教程，亮点：
- **Volatility2 docker 方案**：在不支持的 Ubuntu 版本上跑老 vol
- **dwarf2json 方案**：现代 Volatility3 推荐的 ISF JSON profile 生成
- **bip39 钱包恢复**：把 wallet 数据 hex 还原为 12 词助记词

适用读者：内存取证研究员 / 区块链安全工程师 / 应急响应人员
